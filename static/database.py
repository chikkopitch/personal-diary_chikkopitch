import sqlite3
from datetime import date

DATABASE = 'guestbook.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def add_test_messages():
    conn = get_db_connection()
    # Небольшая проверка: добавляем тестовые данные, только если таблица пустая
    count = conn.execute('SELECT COUNT(*) FROM messages').fetchone()[0]
    
    if count == 0:
        conn.execute(
            'INSERT INTO messages (name, message, created_at) VALUES (?, ?, ?)',
            ('Анна', 'Отличный сайт!', '2026-05-28')
        )
        # Дописанный код для второго тестового сообщения
        conn.execute(
            'INSERT INTO messages (name, message, created_at) VALUES (?, ?, ?)',
            ('Иван', 'Всем привет! Это мое первое сообщение.', '2026-05-27')
        )
        conn.commit()
    conn.close()

def init_db():
    conn = get_db_connection()
    # Дописан SQL-запрос для создания полей таблицы
    conn.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at DATE NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    
    # Добавляем тестовые данные (по заданию 3)
    add_test_messages()

def get_all_messages():
    conn = get_db_connection()
    messages = conn.execute(
        'SELECT * FROM messages ORDER BY created_at DESC'
    ).fetchall()
    conn.close()
    return messages