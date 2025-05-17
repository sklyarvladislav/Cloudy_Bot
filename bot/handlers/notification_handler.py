# --- Основные бибилиотеки ---#
from aiogram import types, Router, F
from aiogram.types import Message
from datetime import datetime
import requests
from keyboards.time_kb import (
    menu_ikb,
    cancel_ikb,
    time_exist_ikb,
    no_time_ikb,
    create_times_ikb,
    create_cities_ikb,
    city_exist_ikb,
    city_not_exist_ikb,
)

# --- Библиотеки состояния ---#
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command

# --- База данных ---#
from database.db import (
    set_user_time_db,
    get_user_time_db,
    get_user_time_btn_db,
    delete_user_time_db,
    set_user_city_db,
    get_user_city_db,
    delete_user_city_db,
)

# Прокладка маршрута
time_router = Router()


# Реализация состояний
class Time(StatesGroup):
    fix_user_time = State()
    delete_time = State()
    fix_user_city = State()


# --- Время для вывода ---#
user_date = datetime.now()
user_t = int(user_date.strftime("%H"))


# -------- Настройка уведомлений --------#
@time_router.message(Command("time"))
async def time_manipulation(message: Message):
    user_id = message.from_user.id
    countTimes = get_user_time_db(user_id)
    user_set_city = get_user_city_db(user_id)

    await message.answer(
        f"*Настройка уведомлений 🔧\n*"
        "• Лимит городов: 1\n"
        "• Лимит времен для отправки сообщений: *3*\n\n"
        f"🏙Текущий город: *{user_set_city if user_set_city else "отсутствует"}*\n"
        f"💬Время уведомлений: *{countTimes}*",
        reply_markup=menu_ikb,
        parse_mode="Markdown",
    )


# --- Блок с ручным вводом времени ---#
@time_router.callback_query(F.data == "set_user_time")
async def set_user_time_button(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "Установите удобное вам время в формате ЧЧ:ММ (например, 12:00)"
    )

    # установим состояние
    await state.set_state(Time.fix_user_time)


# Обрабатываем полученное время
@time_router.message(Time.fix_user_time)
async def save_user_time(message: Message, state: FSMContext):
    user_set_time = message.text.strip()

    # Проверка на корректность времени
    if (
        len(user_set_time) == 5
        and user_set_time[2] == ":"
        and user_set_time.replace(":", "").isdigit()
        and int(user_set_time[:2]) <= 23
        and int(user_set_time[-2:]) <= 59
    ):
        success_db_answer = set_user_time_db(
            user_id=message.from_user.id, time=user_set_time
        )

        if success_db_answer:
            await message.delete()
            await message.answer(
                f"Отлично, теперь отчет по погоде будет приходить вам в *{user_set_time}* ⛅️",
                parse_mode="Markdown",
            )

            await state.clear()
        else:
            await message.answer(
                "❌ Превыщение количества времен/повторяетя время."
                " Удалите одно из имеющихся, чтобы добавить новое или повторите ввод",
                reply_markup=time_exist_ikb,
            )

    else:
        await message.answer(
            "❌ Неверный формат. Пожалуйста, введите время в формате ЧЧ:ММ (например, 12:00)",
            reply_markup=cancel_ikb,
        )


# --- Обработка отмены действия ---#
@time_router.callback_query(F.data == "cancel_action")
async def cancel_action(callback: types.CallbackQuery, state: FSMContext):
    # чистим за собой сообщение
    await callback.message.delete()

    # выходим из состояния
    await state.clear()


# --- Блок с удалением времени --- #
@time_router.callback_query(F.data == "delete_time")
async def ask_to_delete_time(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    times = get_user_time_btn_db(user_id)

    if not times:
        await callback.message.answer(
            "❗️У вас отсутствует установленное время❗️", reply_markup=no_time_ikb
        )
        await state.clear()
    else:
        generate_time_ikb = create_times_ikb(times)
        await callback.message.answer(
            "Выберите время для удаления:", reply_markup=generate_time_ikb
        )
        await state.set_state(Time.delete_time)


# --- Обработка удаления конкретного времени --- #
@time_router.callback_query(Time.delete_time, F.data.startswith("delete_"))
async def delete_set_time(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    time_to_delete = callback.data.replace("delete_", "")

    delete_user_time_db(user_id, time_to_delete)

    await callback.message.delete()
    await callback.message.answer(
        f"Время *{time_to_delete}* удалено ✅", parse_mode="Markdown"
    )
    await state.clear()


# --- Блок с выбором города ---#
@time_router.callback_query(F.data == "set_users_city")
async def set_user_city_button(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("По какому городу хотите получать отчет:")
    await state.set_state(Time.fix_user_city)


@time_router.message(Time.fix_user_city)
async def save_user_city(message: Message, state: FSMContext):
    user_city = message.text.strip().title()

    check_city_url = "https://nominatim.openstreetmap.org/search"
    params = {"q": user_city, "format": "json", "limit": 2}
    headers = {"User-Agent": "Weather_bot"}

    # Проверка города на существование
    try:
        response = requests.get(check_city_url, params=params, headers=headers)
        check_city_data = response.json()
    except Exception:
        await state.clear()
        return await message.answer(
            "Произошла ошибка при подключении. Попробуйте позже."
        )

    if not check_city_data:
        return await message.answer(
            "Город не найден, попробуйте ещё раз", reply_markup=cancel_ikb
        )

    # Для генерации кнопок
    cities_btn = []

    # Переберем города и выведем пользователю
    for city in check_city_data:
        display_name = city.get("display_name", "")
        city_parts = display_name.split(", ")
        if len(city_parts) >= 2:
            cities_btn.append(f"{city_parts[0]}, {city_parts[1]}")

    # Сгенерируем кнопки
    generate_city_ikb = create_cities_ikb(cities_btn)
    await message.answer("Выберите подходящий город", reply_markup=generate_city_ikb)

    await state.set_state(Time.fix_user_city)


# Сохранение в бд
@time_router.callback_query(Time.fix_user_city, F.data.startswith("add_"))
async def add_city_in_db(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    city = callback.data.replace("add_", "")

    # Попробуем сохранить в бд
    success = set_user_city_db(user_id, city)

    await callback.message.delete()

    if success:
        await callback.message.answer(
            f"Отчет о погоде будет приходить по городу: *{city}*", parse_mode="Markdown"
        )
    else:
        current_city = get_user_city_db(user_id)
        await callback.message.answer(
            f"У вас уже установлен город: {current_city}",
            parse_mode="Markdown",
            reply_markup=city_exist_ikb,
        )

    await state.clear()


# Удаление города
@time_router.callback_query(F.data == "delete_users_city")
async def delete_city(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    city = get_user_city_db(user_id)

    if city is None:
        await callback.message.answer(
            "Город не установлен", reply_markup=city_not_exist_ikb
        )
    else:
        delete_user_city_db(user_id, city)
        await callback.message.delete()
        await callback.message.answer(
            "Город удален, отчеты больше не будут приходить ✅"
        )
        await state.clear()
