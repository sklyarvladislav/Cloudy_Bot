#--- Основные бибилиотеки ---#
import asyncio

#--- Отслеживание состояния --#
# from sheduler import scheduler, schedule_weather_jobs
from aiogram import Bot, Dispatcher

#--- Файлы с функциями ---#
import handlers.notification_handler as notification_handler
import handlers.get_weather_handler as get_weather_handler
import handlers.start_handler as start_handler

#--- Токен из config ---#
from config import BOT_TOKEN


#--- Запуск бота ---#
async def main():
    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(notification_handler.time_router)
    dp.include_router(get_weather_handler.get_w_router)
    dp.include_router(start_handler.start_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())


    