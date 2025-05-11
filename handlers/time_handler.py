#--- Основные бибилиотеки ---#
from aiogram import types, Router, F
from aiogram.types import Message
from datetime import datetime, timezone
from keyboards.time_kb import(menu_ikb, cansel_ikb,
                              has_time_ikb, no_time_ikb)

#--- Библиотеки состояния ---#
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command

#--- База данных ---#
from database.db import set_user_time, get_user_time, delete_user_time

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
    user_set_time = get_user_time(message.from_user.id)
    countTimes = ", ".join(user_set_time) if user_set_time else "отсутствует"

    await message.answer(f"*Настройка уведомлений 🔧\n*" \
                         "1. Выбрать предложенное время\n" \
                         "2. Установить собственное время\n" \
                         "3. Просмотреть установленное время\n" \
                         "4. Удалить время\n\n" \
                         f"💬Время уведомлений: *{countTimes}*", reply_markup = menu_ikb, parse_mode = "Markdown")


#--- Блок с ручным вводом времени ---#
@time_router.callback_query(F.data == "set_user_time")
async def second_time_command(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Установите удобное вам время в формате ЧЧ:ММ (например, 12:00)")

    # установим состояние 
    await state.set_state(Time.user_time)


# обрабатываем полученное время
@time_router.message(Time.user_time)
async def save_user_time(message: Message, state: FSMContext):
    
    user_set_time = message.text # сохраним время в переменную

    try:
        # проверка на корректность времени
        if (len(user_set_time) == 5 and
            user_set_time[2] == ":" and
            user_set_time.replace(":", "").isdigit() and
            int(user_set_time[:2]) <= 23 and 
            int(user_set_time[-2:]) <= 59):

            # сохраним id и время в базу данных
            try:
                set_user_time(user_id = message.from_user.id, time = user_set_time)
            except Exception:
                await message.answer("Превышен лимит по количеству времен")

            await message.answer(f"Отлично, теперь отчет по погоде будет приходить вам в *{user_set_time}* ⛅️",
                                  parse_mode="Markdown")
        else:
            raise ValueError
        
        await state.clear()
    except Exception as e:
        print(e)
        await message.answer("❌ Неверный формат. Пожалуйста, введите время в формате ЧЧ:ММ (например, 12:00)", reply_markup = cansel_ikb)

#--- Обработка отмены действия ---#
@time_router.callback_query(F.data == "cansel_action")
async def cansel_action(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("Успешно!")
    await state.clear()


#--- Блок с удалением времени ---#
@time_router.callback_query(F.data == "delete_time")
async def delete_time(callback: types.CallbackQuery, state = FSMContext):
    user_set_time = get_user_time(callback.from_user.id)
    countTimes = ", ".join(user_set_time)

    if(user_set_time == None):
        await callback.message.answer("❗️У вас отсутствует установленное время❗️", reply_markup = no_time_ikb)
        await state.clear()
    else:    
        await callback.message.answer(f"Ваше последнее установленное время: {countTimes}", reply_markup = has_time_ikb)
        

# Обрабытваем удаление времени
@time_router.callback_query(F.data == "delete_set_time")
async def delete_set_time(callback: types.CallbackQuery):
    # удаляем время
    delete_user_time(user_id = callback.from_user.id)

    # ответим
    await callback.answer("Ваше время успешно удалено")
    