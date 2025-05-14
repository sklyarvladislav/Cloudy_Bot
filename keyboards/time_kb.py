from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

#--- Клавиатура меню ---#
menu_ikb = InlineKeyboardMarkup(inline_keyboard = [
        [InlineKeyboardButton(text = "Установить время", callback_data = "set_user_time"),
         InlineKeyboardButton(text = "Выбрать город", callback_data = "set_users_city")],

        [InlineKeyboardButton(text = "Удалить время", callback_data = "delete_time"),
         InlineKeyboardButton(text = "Удалить город", callback_data = "delete_users_city")],

        [InlineKeyboardButton(text = "Отменить действие", callback_data = "cansel_action")]])

# отменить действие
cansel_ikb = InlineKeyboardMarkup(inline_keyboard = [[InlineKeyboardButton(text = "Отменить действие", callback_data = "cansel_action")]])

# удалить время + отменить действие
has_time_ikb = InlineKeyboardMarkup(inline_keyboard = [[InlineKeyboardButton(text = "Удалить время", callback_data = "delete_set_time"),
                                                        InlineKeyboardButton(text = "Отменить действие", callback_data = "cansel_action")]])

# Пи отсутствие времени
no_time_ikb = InlineKeyboardMarkup(inline_keyboard = [
              [InlineKeyboardButton(text = "Установить свое время", callback_data = "set_user_time")],
              [InlineKeyboardButton(text = "Отменить действие", callback_data = "cansel_action")] ])

# Создание клавиатуры через цикл для времени
def create_times_ikb(times: list[str]) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=time, callback_data=f"delete_{time}")]
        for time in times
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

#--- ---#
def create_cities_ikb(cities: str) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text = city, callback_data = f"add_{city}")]
        for city in cities
    ]
    return InlineKeyboardMarkup(inline_keyboard = buttons) 
    