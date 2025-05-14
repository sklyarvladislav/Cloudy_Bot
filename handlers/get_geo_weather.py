import requests
from aiogram.types import Message
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram import Router, F, types

#--- Библиотеки состояния ---#
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command

#--- Импорт из time ---#
from handlers.notification_handler import grinvich_t, user_t

#--- Передача API-ключа ---#
from config import WEATHER_API_KEY

# для прокладки маршрута
get_w_router = Router()

# класс состояния
class UserGeo(StatesGroup):
    get_weather_geo = State()

# приветствия
greetings = ['Доброе утро', 'Добрый день', 'Добрый вечер', 'Доброй ночи']


# обработка события inline-кнопки
@get_w_router.callback_query(F.data == "get_user_geo")
async def request_location(callback: types.CallbackQuery, state: FSMContext):
    # После нажатия inline-кнопки — отправляем обычную кнопку с запросом геолокации

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📍 Отправить геопозицию", request_location=True),
            KeyboardButton(text = "Отменить действие")]
            ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await callback.message.answer("Подтвердите отправку геопозиции👇", reply_markup=kb)
    
    await state.set_state(UserGeo.get_weather_geo)

#--- Обработка отмены действия ---#
@get_w_router.message(F.text == "Отменить действие")
async def cansel_button_action(message: types.Message, state:FSMContext):
    await message.answer("Отменено")
    await message.delete()
    await state.clear()

#--- Отправим погоду по геопозиции ---#
@get_w_router.message(F.location, UserGeo.get_weather_geo)
async def handle_location(message: types.Message, state: FSMContext):
    # сохраняем долготу и широту
    lat = message.location.latitude
    lon = message.location.longitude

    try:
        user_location_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&lang=ru&appid={WEATHER_API_KEY}"
        user_location_data = requests.get(user_location_url).json()

        # Достаем нужные данные
        local_temp = round(user_location_data['main']['temp'])
        local_temp_feel = round(user_location_data['main']['feels_like'])
        wind = round(user_location_data['wind']['speed'])
        humidity = round(user_location_data['main']['humidity'])
        city_name = user_location_data['name']
        local_utc = round(user_location_data['timezone']) // 3600

        # Обрабатываем местное время
        if int(grinvich_t.strftime('%H')) + local_utc > 24:
            konvert_utc = (int(grinvich_t.strftime('%H')) + local_utc) - 24
        else:
            konvert_utc = int(grinvich_t.strftime('%H')) + local_utc

        fin_utc = f"{konvert_utc}:{grinvich_t.strftime('%M')}"

        # Определяем приветствие
        if user_t >= 4 and user_t < 12:
            i = 0
        elif user_t >= 12 and user_t < 18:
            i = 1
        elif user_t >= 18 and user_t < 21:
            i = 2
        else:
            i = 3

        await message.answer(f"{greetings[i]}, {message.from_user.full_name}!\n"
                             f"Погода в городе {city_name}\n\n"
                             "Текущие данные:\n"
                             f"Местное время: {fin_utc}\n"
                             f"Температура: {local_temp}°C\n"
                             f"Ощущается как: {local_temp_feel}°C\n"
                             f"Влажность: {humidity}%\n"
                             f"Ветер: {wind} м/с")

        await state.clear()

    except Exception as e:
        print(e)
        await message.answer("Произошла ошибка в определении геопозиции!\nПопробуйте ещё раз или введите название населенного пункта вручную")
        await state.clear()
