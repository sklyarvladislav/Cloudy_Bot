# from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from apscheduler.triggers.cron import CronTrigger
# from aiogram import Bot
# import asyncio
#
# from database.db import get_all_user_times_and_cities
# from utils.weather import get_weather_data_by_city
#
# scheduler = AsyncIOScheduler()
#
#
# async def send_weather_report(bot: Bot, user_id: int, city: str):
#     try:
#         report = await get_weather_data_by_city(city)
#         await bot.send_message(user_id, report)
#     except Exception as e:
#         print(f"[!] Ошибка при отправке отчета пользователю {user_id}: {e}")
#
#
# async def schedule_weather_jobs(bot: Bot):
#     """
#     Создает задания на отправку прогноза погоды по временам из базы.
#     Один пользователь может иметь несколько времен (или ни одного).
#     """
#     data = get_all_user_times_and_cities()  # [(user_id, city, time), ...]
#
#     if not data:
#         print("[!] Нет данных о времени и городах в базе.")
#         return
#
#     for user_id, city, time_str in data:
#         try:
#             hour, minute = map(int, time_str.split(":"))
#             trigger = CronTrigger(hour = hour, minute = minute)
#
#             job_id = f"{user_id}_{city}_{time_str}"
#
#             scheduler.add_job(
#                 lambda bot = bot, user_id=user_id, city=city: asyncio.create_task(
#                     send_weather_report(bot, user_id, city)
#                 ),
#                 trigger=trigger,
#                 id=job_id,
#                 replace_existing=True
#             )
#             print(f"[+] Задача добавлена: {job_id}")
#         except Exception as e:
#             print(f"[!] Ошибка при добавлении задачи {user_id=} {city=} {time_str=}: {e}")
