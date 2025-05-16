from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

#--- Клавиатура меню ---#
menu_ikb = InlineKeyboardMarkup(inline_keyboard = [
        [InlineKeyboardButton(text = "Установить время", callback_data = "set_user_time"),
         InlineKeyboardButton(text = "Выбрать город", callback_data = "set_users_city")],

        [InlineKeyboardButton(text = "Удалить время", callback_data = "delete_time"),
         InlineKeyboardButton(text = "Удалить город", callback_data = "delete_users_city")],

        [InlineKeyboardButton(text = "↩️ Отменить действие", callback_data = "cancel_action")]])

# Отменить действие
cancel_ikb = InlineKeyboardMarkup(inline_keyboard = [[InlineKeyboardButton(text = "↩️ Отменить действие", callback_data = "cancel_action")]])

#--- Блок времени ---#

# Удалить время + Отменить действие
time_exist_ikb = InlineKeyboardMarkup(inline_keyboard = [[InlineKeyboardButton(text = "🗑 Удалить время", callback_data = "delete_time"),
                                                        InlineKeyboardButton(text = "↩️ Отменить действие", callback_data = "cancel_action")]])

# При отсутствие времени
no_time_ikb = InlineKeyboardMarkup(inline_keyboard = [
              [InlineKeyboardButton(text = "📌 Установить время", callback_data = "set_user_time")],
              [InlineKeyboardButton(text = "↩️Отменить действие", callback_data = "cancel_action")] ])

# Генерация кнопок со временем
def create_times_ikb(times: list[str]) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text = time, callback_data = f"delete_{time}")]
        for time in times
    ]

    buttons.append([InlineKeyboardButton(text="↩️ Отменить действие", callback_data="cancel_action")])
    return InlineKeyboardMarkup(inline_keyboard = buttons)

#--- Блок города ---#

# Генерация кнопок с городами
def create_cities_ikb(cities: list[str]) -> InlineKeyboardMarkup:
    buttons = []

    for city in cities:
        if "," in city:
            region = city.split(",")[1].strip()
        else:
            region = city.strip()
        buttons.append([InlineKeyboardButton(text=city, callback_data=f"add_{region}")])

    # Добавляем кнопку отмены в конце
    buttons.append([InlineKeyboardButton(text="↩️ Отменить действие", callback_data="cancel_action")])

    return InlineKeyboardMarkup(inline_keyboard = buttons)
    
# Если город установлен/не установлен
city_exist_ikb = InlineKeyboardMarkup(inline_keyboard = [[InlineKeyboardButton(text = "🗑 Удалить город", callback_data = "delete_users_city"),
                                                        InlineKeyboardButton(text = "↩️ Отменить действие", callback_data = "cancel_action")]])

city_not_exist_ikb = InlineKeyboardMarkup(inline_keyboard = [[InlineKeyboardButton(text = "📌 Установить город", callback_data = "set_users_city"),
                                                        InlineKeyboardButton(text = "↩️ Отменить действие", callback_data = "cancel_action")]])