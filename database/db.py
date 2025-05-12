import sqlite3

conn = sqlite3.connect("bot_database.db")
cursor = conn.cursor()


# добавить время
def set_user_time(user_id: int, time: str) -> bool:
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()

    # проверяем количество уже сохранённых времён
    cursor.execute("SELECT COUNT(*) FROM users_time WHERE user_id = ?", (user_id,))
    count_times = cursor.fetchone()[0]

    if count_times >= 3:
        conn.close()
        return False  # пользователь превысил лимит

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
    cursor.execute('SELECT time FROM users_time WHERE user_id = ?', (user_id,))
    times = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    return ', '.join(times) if times else 'отсутствует'

# запросить время по id для кнопок
def get_user_time_list(user_id: int) -> list[str]:
    conn = sqlite3.connect("bot_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT time FROM users_time WHERE user_id = ?", (user_id,))
    times = [row[0] for row in cursor.fetchall()]
    conn.close()
    return times

# удалить время
def delete_user_time(user_id: int, time: str):
    conn = sqlite3.connect("bot_database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users_time WHERE user_id = ? AND time = ?", (user_id, time))
    conn.commit()
    conn.close()
