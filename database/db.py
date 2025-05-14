import sqlite3

conn = sqlite3.connect("bot_database.db")
cursor = conn.cursor()

#--- Хранение времен пользователя ---#

# Добавить время
def set_user_time(user_id: int, time: str) -> bool:
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()

    # проверяем количество уже сохранённых времён
    cursor.execute("SELECT COUNT(*) FROM users_time WHERE user_id = ?", (user_id,))
    count_times = cursor.fetchone()[0]

    # пользователь превысил лимит
    if count_times >= 3:
        conn.close()
        return False

    cursor.execute('''
        INSERT INTO users_time(user_id, time) VALUES (?, ?)
    ''', (user_id, time))
    conn.commit()
    conn.close()
    return True


# запросить время по id для вывода пользователю
def get_user_time(user_id: int) -> str:
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT time FROM users_time WHERE user_id = ?", (user_id,))
    times = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    return ', '.join(times) if times else 'отсутствует'

# Запросить время по id для кнопок
def get_user_time_list(user_id: int) -> list[str]:
    conn = sqlite3.connect("bot_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT time FROM users_time WHERE user_id = ?", (user_id,))
    times = [row[0] for row in cursor.fetchall()]
    conn.close()
    return times

# Удалить время
def delete_user_time(user_id: int, time: str):
    conn = sqlite3.connect("bot_database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users_time WHERE user_id = ? AND time = ?", (user_id, time))
    conn.commit()
    conn.close()


#--- Хранение города для погоды ---#

# Добавить город
def set_user_city(user_id: int, city: str) -> bool:
    conn = sqlite3.connect("bot_database.db")
    cursor = conn.cursor()

    # проверим сколько городов уже хранится
    cursor.execute("SELECT COUNT(*) FROM users_city WHERE user_id = ?", (user_id, ))
    count_city = cursor.fetchone()[0]

    # превышение лимита
    if count_city >= 1:
        conn.close()
        return False
    
    cursor.execute(''' 
            INSERT INTO users_city(user_id, city) VALUES (?, ?)
    ''', (user_id, city))

    conn.commit()
    conn.close()
    return True 

# Вывод текущего города
def get_user_city(user_id: int) -> str:
    conn = sqlite3.connect("bot_database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT city FROM users_city WHERE user_id = ?", (user_id,))
    city = cursor.fetchall()

    conn.close()
    return city if city else "отсутствует"

# Удаление города 
def delete_user_city(user_id: int, city: str):
    conn = sqlite3.connect("bot_database.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users_city WHERE user_id = ? AND city = ?", (user_id, city))
    conn.commit()

    conn.close()



