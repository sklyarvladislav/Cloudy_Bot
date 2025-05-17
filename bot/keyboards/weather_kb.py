from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


geolocation_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📍 Отправить геопозицию", request_location=True),
            KeyboardButton(text="↩️ Отменить действие"),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

# кнопка для геопозиции
start_message_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Погода в моем городе 🌥️", callback_data="get_user_geo"
            )
        ]
    ]
)
