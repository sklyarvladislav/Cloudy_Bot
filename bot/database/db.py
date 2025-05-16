import sqlite3

conn = sqlite3.connect("bot_database.db")
cursor = conn.cursor()


#--- Хранение времен пользователя ---#

# Добавить время
def set_user_time_db(user_id: int, time: str) -> bool:
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()

    # Проверка: время уже существует у пользователя?
    cursor.execute("SELECT 1 FROM users_time WHERE user_id = ? AND time = ? LIMIT 1",
                  (user_id, time)
                  )
    
    if cursor.fetchone():
        conn.close()
        return False  # Время уже добавлено

    # Проверка лимита (считаем только если время ещё не добавлено)
    cursor.execute("SELECT COUNT(*) FROM users_time WHERE user_id = ?",
                  (user_id,)
                  )

    count_times = cursor.fetchone()[0]

    if count_times >= 3:
        conn.close()
        return False  # Лимит превышен

    # Добавление нового времени
    cursor.execute("INSERT INTO users_time(user_id, time) VALUES (?, ?)",
                  (user_id, time)
                  )
    
    conn.commit()
    conn.close()
    return True



# Запросить время по id для вывода пользователю
def get_user_time_db(user_id: int) -> str:
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT time FROM users_time WHERE user_id = ?", (user_id,))
    times = [row[0] for row in cursor.fetchall()]

    conn.close()
    return ', '.join(times) if times else 'отсутствует'

# Запросить время по id для кнопок
def get_user_time_btn_db(user_id: int) -> list[str]:
    conn = sqlite3.connect("bot_database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT time FROM users_time WHERE user_id = ?", (user_id,))
    times = [row[0] for row in cursor.fetchall()]

    conn.close()
    return times

# Удалить время
def delete_user_time_db(user_id: int, time: str):
    conn = sqlite3.connect("bot_database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users_time WHERE user_id = ? AND time = ?", (user_id, time))
    conn.commit()
    conn.close()


#--- Хранение города для погоды ---#

# Добавить город
def set_user_city_db(user_id: int, city: str) -> bool:
    conn = sqlite3.connect("bot_database.db")
    cursor = conn.cursor()

    # проверим сколько городов уже хранится
    cursor.execute("SELECT COUNT(*) FROM users_city WHERE user_id = ?", (user_id,))
    count_city = cursor.fetchone()[0]

    # превышение лимита
    if count_city >= 1:
        conn.close()
        return False
    
    cursor.execute("INSERT INTO users_city(user_id, city) VALUES (?, ?)", (user_id, city))

    conn.commit()
    conn.close()
    return True 

# Вывод текущего города
def get_user_city_db(user_id: int) -> str | None:
    conn = sqlite3.connect("bot_database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT city FROM users_city WHERE user_id = ?", (user_id,))
    city = cursor.fetchone()

    conn.close()
    return city[0] if city else None

# Удаление города 
def delete_user_city_db(user_id: int, city: str):
    conn = sqlite3.connect("bot_database.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users_city WHERE user_id = ? AND city = ?", (user_id, city))
    conn.commit()

    conn.close()

# # Для sheduller
# def get_all_user_times_and_cities():
#     conn = sqlite3.connect("bot_database.db")
#     cursor = conn.cursor()

#     cursor.execute("""
#         SELECT ut.user_id, uc.city, ut.time
#         FROM users_time ut
#         JOIN users_city uc ON ut.user_id = uc.user_id
#     """)
#     results = cursor.fetchall()
#     conn.close()

#     return results  # список кортежей: (user_id, city, time)


