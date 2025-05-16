#--- Основные библиотеки ---#
from aiogram.types import Message
from aiogram import Router, F, types

#--- Библиотеки состояния ---#
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import StateFilter

#--- Imports из файлов ---#
from keyboards.weather_kb import geolocation_kb
from utils.weather import get_weather_data_by_coords, get_weather_data_by_city

# Прокладка маршрута
get_w_router = Router()

# Класс состояния
class UserGeo(StatesGroup):
    get_weather_geo = State()
    

#--- Получение погоды по введеному городу ---#
@get_w_router.message(~F.text.startswith("/"), StateFilter(None))
async def get_weather(message: Message, state: FSMContext):
    # получаем текущее состояние
    current_state = await state.get_state()

    # если его нет, то переходим к выводу погоды
    if current_state in ["Time:setting_time", "Time:user_time",
                          "Time:delete_time","UserGeo:get_weather_geo"]:
        return
    
    # Получаем название города из сообщения
    main_city = message.text

    try:
        weather = await get_weather_data_by_city(main_city)
        
        await message.answer(f"{weather['greeting']}, *{message.from_user.full_name}*!\n"
                             f"Погода в городе {weather['city']}\n\n"
                              "Текущие данные\n"
                             f"Местное время: {weather['time']}\n"
                             f"Температура: {weather['temp']}°C\n"
                             f"Ощущается как: {weather['feels_like']}°C\n"
                             f"Влажность: {weather['humidity']}%\n"
                             f"Ветер: {weather['wind']} м/с",
                             parse_mode = "Markdown")             
    except Exception as e:
        print(e)
        await message.answer("Ошибка! Проверьте название города и попробуйте еще раз 🔄")


#--- Вывод погоды по геопозиции---#

# Считываем событие Inline кнопки
@get_w_router.callback_query(F.data == "get_user_geo")
async def request_location(callback: types.CallbackQuery, state: FSMContext):

    # После нажатия inline-кнопки — отправляем обычную кнопку с запросом геолокации
    await callback.message.answer("Подтвердите отправку геопозиции👇", reply_markup = geolocation_kb)
    
    await state.set_state(UserGeo.get_weather_geo)


# Отправим погоду по геопозиции
@get_w_router.message(F.location, UserGeo.get_weather_geo)
async def handle_location(message: types.Message, state: FSMContext):
    # Долгота и широта пользователя
    lat = message.location.latitude
    lon = message.location.longitude

    # Пробуем узнать погоду по координатам
    try:
        weather = await get_weather_data_by_coords(lat, lon)

        await message.answer(f"{weather['greeting']}, *{message.from_user.full_name}*!\n"
                             f"Погода в городе {weather['city']}\n\n"
                              "Текущие данные\n"
                             f"Местное время: {weather['time']}\n"
                             f"Температура: {weather['temp']}°C\n"
                             f"Ощущается как: {weather['feels_like']}°C\n"
                             f"Влажность: {weather['humidity']}%\n"
                             f"Ветер: {weather['wind']} м/с",
                             parse_mode = "Markdown")
        await state.clear()
    except Exception as e:
        print(e)
        await message.answer("К сожалению, геопозиция не определилась. "/
                             "Попробуйтет ввести город вручную 😔")
        await state.clear()


#--- Отмена действия ---#
@get_w_router.message(F.text == "Отменить действие")
async def cansel_button_action(message: types.Message, state:FSMContext):
    await message.delete()
    await state.clear()