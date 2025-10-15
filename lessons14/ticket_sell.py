import sqlite3

# Підключення до SQLite
conn = sqlite3.connect("tickets_sqlite.db")
cursor = conn.cursor()

# Створення таблиць
cursor.executescript("""
DROP TABLE IF EXISTS tickets;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS events;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);

CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    location TEXT,
    date DATE
);

CREATE TABLE tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    event_id INTEGER,
    price REAL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (event_id) REFERENCES events(id)
);
""")

# Дані
users = [
    ("Андрій Шевченко", "andriy@example.com"),
    ("Олена Коваль", "olena@example.com"),
    ("Ігор Бондар", "ihor@example.com")
]

events = [
    ("Концерт 'Океан Ельзи'", "Київ", "2025-11-01"),
    ("Театральна вистава", "Львів", "2025-11-05"),
    ("Бізнес-конференція", "Харків", "2025-11-10")
]

tickets = [
    (1, 1, 600.00),
    (2, 1, 550.00),
    (3, 1, 620.00),
    (1, 2, 300.00),
    (2, 2, 350.00),
    (3, 3, 700.00),
    (1, 3, 800.00),
    (2, 3, 500.00),
    (3, 1, 580.00),
    (1, 1, 610.00)
]

# Вставка даних
cursor.executemany("INSERT INTO users (name, email) VALUES (?, ?);", users)
cursor.executemany("INSERT INTO events (title, location, date) VALUES (?, ?, ?);", events)
cursor.executemany("INSERT INTO tickets (user_id, event_id, price) VALUES (?, ?, ?);", tickets)

# !!! ЗБЕРЕГТИ ЗМІНИ
conn.commit()

# Перевірка — виведення користувачів
cursor.execute("SELECT * FROM users;")
print("Користувачі:")
for row in cursor.fetchall():
    print(row)

# Перевірка — виведення квитків
cursor.execute("""
SELECT tickets.id, users.name, events.title, tickets.price
FROM tickets
JOIN users ON tickets.user_id = users.id
JOIN events ON tickets.event_id = events.id;
""")
print("\nКвитки:")
for row in cursor.fetchall():
    print(row)

# Закриття з'єднання
conn.close()
