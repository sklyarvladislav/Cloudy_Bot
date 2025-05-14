#--- Основные бибилиотеки ---#
import requests
import asyncio
from aiogram.types import Message
from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

#--- Отслеживание состояния --#
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

#--- Файлы с функциями ---#
import handlers.notification_handler as notification_handler
from handlers.notification_handler import grinvich_t, user_t
import handlers.get_geo_weather as get_geo_weather

#--- Передадим приветствия ---#
from handlers.get_geo_weather import greetings

#--- Токен и API-ключи из config ---#
from config import BOT_TOKEN, WEATHER_API_KEY

# Передадим токены и маршрут
bot = Bot(BOT_TOKEN)
dp = Dispatcher()
dp.include_router(notification_handler.time_router)
dp.include_router(get_geo_weather.get_w_router)



#--- Блок /start ---#
@dp.message(Command("start"))
async def start_command(message: Message):

    # кнопка для геопозиции
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Погода в моем городе 🌥️", callback_data="get_user_geo")]
    ])

    await message.answer(f"Привет, {message.from_user.full_name}. " \
                         f"Чтобы узнать погоду, напишите название города или дайте доступ к геопозиции\n\n" +
                          f"_❗️О выводе погоды по геопозиции❗️\n_" \
                          f"*1.* Функция недоступна для ПК\n" + 
                          f"*2.* Telegram слишком точно определяет вашу геопозицию," + 
                          " поэтому иногда может показывать погоду не города, а вашего района",
                           reply_markup=ikb, parse_mode = "Markdown")
    


#--- Блок получения погоды по введеному городу ---#
@dp.message(~F.text.startswith("/"), StateFilter(None))
async def get_weather(message: Message, state: FSMContext):
    # получаем текущее состояние
    current_state = await state.get_state()

    # если его нет, то переходим к выводу погоды
    if current_state in ["Time:setting_time", "Time:user_time",
                          "Time:delete_time","UserGeo:get_weather_geo"]:
        return

    # Получаем название города из сообщения
    main_city = message.text

    # вставляем название города в запрос
    url = f"http://api.openweathermap.org/data/2.5/weather?q={main_city}&lang=ru&units=metric&appid={WEATHER_API_KEY}"
    
    # пробуем достать данные и вывести их
    try:
        data = requests.get(url).json()  # Получение ответа API

        # Достаем параметры погоды
        local_utc = round(data['timezone']) // 3600  # Часовой пояс

        # конвертируем время и проверяем не больше ли оно 24 часов?
        if int(grinvich_t.strftime('%H')) + local_utc > 24:
            konvert_utc = (int(grinvich_t.strftime('%H')) + local_utc ) - 24
        elif int(grinvich_t.strftime('%H')) + local_utc == 24:
            konvert_utc = "00"
        else:
            konvert_utc = int(grinvich_t.strftime('%H')) + local_utc

        # собираем итоговое время
        fin_utc = f"{konvert_utc}:{grinvich_t.strftime('%M')}"

        local_temp = round(data['main']['temp']) # темпуратура
        local_temp_feel = round(data['main']['feels_like']) # темпуратура по ощущ.
        wind = round(data['wind']['speed']) # скорость ветра
        humidity = round(data['main']['humidity']) # влажность
        

        # Определяем приветствие и берем из набора приветствий
        if user_t >= 4 and user_t < 12:
            i = 0
        elif user_t >= 12 and user_t < 18:
            i = 1
        elif user_t >= 18 and user_t < 21:
            i = 2
        else:
            i = 3

        # Отправляем сообщение
        await message.answer(f"{greetings[i]}, {message.from_user.full_name}!\n"
                             f"Погода в городе *{main_city.title()}*\n\n"
                             "Текущие данные:\n"
                             f"Местное время: {fin_utc}\n"
                             f"Температура: {local_temp}°C\n"
                             f"Ощущаеся как: {local_temp_feel}°C\n"
                             f"Влажность воздуха: {humidity}%\n"
                             f"Ветер: {wind} м/с", parse_mode = "Markdown")
                     
    except Exception as e:
        print(e)
        await message.answer("Ошибка! Проверьте название города и попробуйте еще раз 🔄")

#--- Запуск бота ---#
async def main():
    async with bot:
        await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
