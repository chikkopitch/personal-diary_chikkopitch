import sqlite3

# ==========================================
# ЧАСТЬ 1: РАБОТА С ТАБЛИЦЕЙ users
# ==========================================

print("--- ЗАДАНИЕ 2: Подключение ---")
conn = sqlite3.connect('mybase.db')
cursor = conn.cursor()
print("База данных создана и подключена!\n")

print("--- ЗАДАНИЕ 3: Создание таблицы users ---")
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL
    )
''')
conn.commit()
print("Таблица users создана!\n")

print("--- ЗАДАНИЕ 4: Добавление данных (INSERT) ---")
# Очистим таблицу перед добавлением, чтобы при повторном запуске данные не дублировались
cursor.execute('DELETE FROM users') 

cursor.execute('''
    INSERT INTO users (name, age) VALUES (?, ?)
''', ('Анна', 25))

users = [
    ('Иван', 30),
    ('Мария', 22),
    ('Петр', 35)
]
cursor.executemany('INSERT INTO users (name, age) VALUES (?, ?)', users)
conn.commit()
print("Пользователи добавлены!\n")

print("--- ЗАДАНИЕ 5: Чтение данных (SELECT) ---")
cursor.execute('SELECT * FROM users')
all_users = cursor.fetchall()
print("Все пользователи:")
for user in all_users:
    print(f"id: {user[0]}, имя: {user[1]}, возраст: {user[2]}")

print("\n--- ЗАДАНИЕ 6: Чтение с условием (WHERE) ---")
cursor.execute('SELECT * FROM users WHERE age > 25')
older_users = cursor.fetchall()
print("Пользователи старше 25:")
for user in older_users:
    print(f"id: {user[0]}, имя: {user[1]}, возраст: {user[2]}")

print("\n--- ЗАДАНИЕ 7: Изменение данных (UPDATE) ---")
cursor.execute('UPDATE users SET age = age + 1')
conn.commit()
cursor.execute('SELECT * FROM users')
updated_users = cursor.fetchall()
print("После увеличения возраста:")
for user in updated_users:
    print(f"id: {user[0]}, имя: {user[1]}, возраст: {user[2]}")

print("\n--- ЗАДАНИЕ 8: Удаление данных (DELETE) ---")
# Удаляем по имени (так как id могут меняться при перезапуске скрипта из-за AUTOINCREMENT)
cursor.execute('DELETE FROM users WHERE name = ?', ('Мария',))
conn.commit()
cursor.execute('SELECT * FROM users')
remaining_users = cursor.fetchall()
print("После удаления Марии:")
for user in remaining_users:
    print(f"id: {user[0]}, имя: {user[1]}, возраст: {user[2]}")


# ==========================================
# ЧАСТЬ 2: РАБОТА С ТАБЛИЦЕЙ products
# ==========================================

print("\n\n--- ЗАДАНИЕ 10: Создание таблицы products ---")
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price INTEGER NOT NULL,
        quantity INTEGER DEFAULT 0
    )
''')
conn.commit()
print("Таблица products создана!")

print("\n--- ЗАДАНИЕ 11: Добавление товаров ---")
# Очищаем таблицу перед вставкой, чтобы избежать дубликатов при тестах
cursor.execute('DELETE FROM products')

products_data = [
    ('Яблоки', 50, 100),
    ('Бананы', 80, 50),
    ('Молоко', 70, 30),
    ('Хлеб', 40, 0),
    ('Сыр', 150, 20)
]
cursor.executemany('''
    INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)
''', products_data)
conn.commit()
print("Товары успешно добавлены!")

print("\n--- ЗАДАНИЕ 12: Вывод всех товаров ---")
cursor.execute('SELECT * FROM products')
all_products = cursor.fetchall()
for p in all_products:
    print(f"{p[0]}. {p[1]} - {p[2]} руб, в наличии: {p[3]}")

print("\n--- ЗАДАНИЕ 13: Товары дешевле 100 рублей ---")
cursor.execute('SELECT * FROM products WHERE price < 100')
cheap_products = cursor.fetchall()
for p in cheap_products:
    print(f"{p[1]}")

print("\n--- ЗАДАНИЕ 14: Товары, которых нет в наличии ---")
cursor.execute('SELECT * FROM products WHERE quantity = 0')
out_of_stock = cursor.fetchall()
for p in out_of_stock:
    print(f"{p[1]}")

print("\n--- ЗАДАНИЕ 15: Увеличиваем цену на 10 рублей ---")
cursor.execute('UPDATE products SET price = price + 10')
conn.commit()
cursor.execute('SELECT * FROM products')
updated_products = cursor.fetchall()
for p in updated_products:
    print(f"{p[1]} - {p[2]} руб")

print("\n--- ЗАДАНИЕ 16: Удаляем товары дороже 100 рублей ---")
cursor.execute('DELETE FROM products WHERE price > 100')
conn.commit()
print("Товары с ценой выше 100 рублей удалены!")

print("\n--- ЗАДАНИЕ 17: Добавляем поле category ---")
try:
    cursor.execute('ALTER TABLE products ADD COLUMN category TEXT DEFAULT "другое"')
except sqlite3.OperationalError:
    # Ошибка сработает, если колонка уже была создана при предыдущем запуске, просто игнорируем её
    pass 

categories_data = [
    ('фрукты', 'Яблоки'),
    ('фрукты', 'Бананы'),
    ('молочные', 'Молоко'),
    ('выпечка', 'Хлеб')
]
cursor.executemany('''
    UPDATE products SET category = ? WHERE name = ?
''', categories_data)
conn.commit()

cursor.execute('SELECT * FROM products')
final_products = cursor.fetchall()
print("Итоговая таблица с категориями:")
for p in final_products:
    print(f"{p[1]} - Категория: {p[4]}")

# ==========================================
# ЗАВЕРШЕНИЕ РАБОТЫ
# ==========================================

print("\n--- ЗАДАНИЕ 9: Закрытие соединения ---")
conn.close()
print("Соединение закрыто.")