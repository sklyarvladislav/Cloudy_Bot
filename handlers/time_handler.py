#--- Основные бибилиотеки ---#
from aiogram import types, Router, F
from aiogram.types import Message
from datetime import datetime, timezone
from keyboards.time_kb import(menu_ikb, cansel_ikb,
                              has_time_ikb, no_time_ikb,
                              create_deleting_ikb)

#--- Библиотеки состояния ---#
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command

#--- База данных ---#
from database.db import (set_user_time, get_user_time,
                        get_user_time_list, delete_user_time)

# для прокладки маршрута
time_router = Router()

# для реализации состояний
class Time(StatesGroup):
    user_time = State()
    delete_time = State()

#--- Время для вывода ---#
user_date = datetime.now()
user_t = int(user_date.strftime('%H'))
grinvich_t = datetime.now(timezone.utc)


#-------- Настройка уведомлений --------#
@time_router.message(Command("time"))
async def time_manipulation(message: Message):
    user_id = message.from_user.id
    countTimes = get_user_time(user_id)

    await message.answer(f"*Настройка уведомлений 🔧\n*" \
                         "1. Установить время\n" \
                         "2. Удалить время\n" \
                         "3. Ограничение времен для отправки сообщений: *3*\n\n"
                         f"💬Время уведомлений: *{countTimes}*",
                         reply_markup = menu_ikb, parse_mode = "Markdown")


#--- Блок с ручным вводом времени ---#
@time_router.callback_query(F.data == "set_user_time")
async def second_time_command(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Установите удобное вам время в формате ЧЧ:ММ (например, 12:00)")

    # установим состояние 
    await state.set_state(Time.user_time)


# обрабатываем полученное время
@time_router.message(Time.user_time)
async def save_user_time(message: Message, state: FSMContext):
    user_set_time = message.text.strip()

    # Проверка на корректность времени
    if (len(user_set_time) == 5 and
        user_set_time[2] == ":" and
        user_set_time.replace(":", "").isdigit() and
        int(user_set_time[:2]) <= 23 and 
        int(user_set_time[-2:]) <= 59):

        success = set_user_time(user_id=message.from_user.id, time=user_set_time)
        
        if success:
            await message.answer(
                f"Отлично, теперь отчет по погоде будет приходить вам в *{user_set_time}* ⛅️",
                parse_mode="Markdown"
            )

            await state.clear()
        else:
            await message.answer(
                "❌ Превыщение количества времен. Удалите одно из имеющихся, чтобы добавить новое",
                reply_markup = has_time_ikb
            )

            await state.clear()
    else:
        await message.answer(
            "❌ Неверный формат. Пожалуйста, введите время в формате ЧЧ:ММ (например, 12:00)",
            reply_markup = cansel_ikb
        )


#--- Обработка отмены действия ---#
@time_router.callback_query(F.data == "cansel_action")
async def cansel_action(callback: types.CallbackQuery, state: FSMContext):
    # чистим за собой сообщение
    await callback.message.delete()

    await callback.answer("Успешно!")
    # выходим из состояния
    await state.clear()


# --- Блок с удалением времени --- #
@time_router.callback_query(F.data == "delete_time")
async def ask_to_delete_time(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    times = get_user_time_list(user_id)

    if not times:
        await callback.message.answer("❗️У вас отсутствует установленное время❗️", reply_markup=no_time_ikb)
        await state.clear()
    else:
        ikb = create_deleting_ikb(times)
        await callback.message.answer("Выберите время для удаления:", reply_markup=ikb)
        await state.set_state(Time.delete_time)

        

# --- Обработка удаления конкретного времени --- #
@time_router.callback_query(Time.delete_time, F.data.startswith("delete_"))
async def delete_set_time(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    time_to_delete = callback.data.replace("delete_", "")

    delete_user_time(user_id, time_to_delete)

    await callback.message.answer(f"Время {time_to_delete} успешно удалено ✅")
    await state.clear()

    