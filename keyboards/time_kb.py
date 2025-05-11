from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

# клавиатура меню
menu_ikb = InlineKeyboardMarkup(inline_keyboard = [
        [InlineKeyboardButton(text = "Установить свое время", callback_data = "set_user_time"),
         InlineKeyboardButton(text = "Удалить время", callback_data = "delete_time")],

         [InlineKeyboardButton(text = "Отменить действие", callback_data = "cansel_action")] ])

# отменить действие
cansel_ikb = InlineKeyboardMarkup(inline_keyboard = [[InlineKeyboardButton(text = "Отменить действие", callback_data = "cansel_action")]])

# удалить время + отменить действие
has_time_ikb = InlineKeyboardMarkup(inline_keyboard = [[InlineKeyboardButton(text = "Удалить время", callback_data = "delete_set_time"),
                                                        InlineKeyboardButton(text = "Отменить действие", callback_data = "cansel_action")]])

# отсутствует время
no_time_ikb = InlineKeyboardMarkup(inline_keyboard = [
              [InlineKeyboardButton(text = "Установить свое время", callback_data = "set_user_time")],
              [InlineKeyboardButton(text = "Отменить действие", callback_data = "cansel_action")] ])

# создание клавиатуры через цикл

# def create_time_kb():
    