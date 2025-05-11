import sqlite3

# --- Создаем или подключаемся к БД ---#
conn = sqlite3.connect("bot_database.db")
cursor = conn.cursor()

# --- Таблица для хранения времени пользователя ---#
cursor.execute('''
CREATE TABLE IF NOT EXISTS users_time (
    user_id INTEGER,
    time TEXT,
    PRIMARY KEY (user_id, time)
)
''')

conn.commit()
conn.close()

# добавить время
def set_user_time(user_id: int, time: str):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()

    #
    cursor.execute("SELECT COUNT(*) FROM users_time WHERE user_id = ?", (user_id,))
    countTimes = cursor.fetchone()[0]

    if countTimes >= 3:
        conn.close()
        raise Exception("Лимит времен превышен")

    cursor.execute('''
                    INSERT INTO users_time(user_id, time) VALUES (?, ?) 
                   ''', (user_id, time))
    conn.commit()
    conn.close()



# запросить время по id
def get_user_time(user_id: int) -> list[str] | None:
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT time FROM users_time WHERE user_id = ?', (user_id, ))

    return [result[0] for result in cursor.fetchall()]


# удалить время
def delete_user_time(user_id: int) -> str | None:
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()

    cursor.execute(''' DELETE FROM users_time WHERE user_id = ?''', (user_id,))
    conn.commit()
    conn.close()