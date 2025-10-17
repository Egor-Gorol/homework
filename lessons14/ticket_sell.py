import sqlite3
import psycopg2

# ------------------------- #
# 1. SQLite — локальна база
# ------------------------- #
sqlite_conn = sqlite3.connect("tickets_sqlite.db")
sqlite_cursor = sqlite_conn.cursor()


sqlite_cursor.execute("DROP TABLE IF EXISTS users")
sqlite_cursor.execute("DROP TABLE IF EXISTS events")
sqlite_cursor.execute("DROP TABLE IF EXISTS tickets")

sqlite_cursor.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT
)
""")
sqlite_cursor.execute("""
CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    location TEXT
)
""")
sqlite_cursor.execute("""
CREATE TABLE tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    event_id INTEGER,
    price REAL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (event_id) REFERENCES events(id)
)
""")


sqlite_cursor.executemany("INSERT INTO users (name, email) VALUES (?, ?)", [
    ("Олег", "oleg@example.com"),
    ("Ірина", "iryna@example.com")
])
sqlite_cursor.executemany("INSERT INTO events (title, location) VALUES (?, ?)", [
    ("Концерт", "Київ"),
    ("Фестиваль", "Львів")
])
sqlite_cursor.executemany("INSERT INTO tickets (user_id, event_id, price) VALUES (?, ?, ?)", [
    (1, 1, 500),
    (2, 1, 600),
    (2, 2, 300)
])

sqlite_conn.commit()

# ------------------------------- #
# 2. PostgreSQL — віддалена база
# ------------------------------- #


PG_USER = "postgres"
PG_PASSWORD = "12345678"
PG_HOST = "localhost"
PG_PORT = "5432"
PG_DBNAME = "tickets_db"

pg_conn = psycopg2.connect(
    dbname=PG_DBNAME,
    user=PG_USER,
    password=PG_PASSWORD,
    host=PG_HOST,
    port=PG_PORT
)
pg_cursor = pg_conn.cursor()


pg_cursor.execute("DROP TABLE IF EXISTS tickets")
pg_cursor.execute("DROP TABLE IF EXISTS users")
pg_cursor.execute("DROP TABLE IF EXISTS events")

pg_cursor.execute("""
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
)
""")
pg_cursor.execute("""
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100),
    location VARCHAR(100)
)
""")
pg_cursor.execute("""
CREATE TABLE tickets (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    event_id INTEGER REFERENCES events(id),
    price NUMERIC
)
""")


pg_cursor.executemany("INSERT INTO users (name, email) VALUES (%s, %s)", [
    ("Наталія", "nata@example.com"),
    ("Артем", "artem@example.com")
])
pg_cursor.executemany("INSERT INTO events (title, location) VALUES (%s, %s)", [
    ("Startup Day", "Харків"),
    ("Jazz Fest", "Одеса")
])
pg_cursor.executemany("INSERT INTO tickets (user_id, event_id, price) VALUES (%s, %s, %s)", [
    (1, 1, 550),
    (2, 2, 800),
    (1, 2, 900)
])

pg_conn.commit()

# ------------------------------- #
# 3. Демонстрація запиту з SQLite
# ------------------------------- #
print("\n[SQLite] Квитки з назвами заходів і іменами користувачів:")
sqlite_cursor.execute("""
SELECT tickets.id, users.name, events.title, tickets.price
FROM tickets
JOIN users ON tickets.user_id = users.id
JOIN events ON tickets.event_id = events.id
""")
for row in sqlite_cursor.fetchall():
    print(row)

# ------------------------------- #
# 4. Демонстрація запиту з PostgreSQL
# ------------------------------- #
print("\n[PostgreSQL] Користувачі, які купили квитки дорожче 600 грн:")
pg_cursor.execute("""
SELECT DISTINCT users.name, users.email
FROM tickets
JOIN users ON tickets.user_id = users.id
WHERE tickets.price > 600
""")
for row in pg_cursor.fetchall():
    print(row)

sqlite_conn.close()
pg_cursor.close()
pg_conn.close()
