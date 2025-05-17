from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router

from keyboards.weather_kb import start_message_ikb

start_router = Router()


# --- Блок /start ---#
@start_router.message(Command("start"))
async def start_command(message: Message):
    await message.answer(
        f"Привет, {message.from_user.full_name}. "
        f"Чтобы узнать погоду, напишите название города или дайте доступ к геопозиции\n\n"
        + "_❗️О выводе погоды по геопозиции❗️\n_"
        "*1.* Функция недоступна для ПК\n"
        + "*2.* Telegram слишком точно определяет вашу геопозицию,"
        + " поэтому иногда может показывать погоду не города, а вашего района",
        reply_markup=start_message_ikb,
        parse_mode="Markdown",
    )
