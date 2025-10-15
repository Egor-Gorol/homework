import sqlite3


conn = sqlite3.connect("restaurants.db")
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS restaurants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    address TEXT NOT NULL,
    michelin_stars INTEGER CHECK(michelin_stars BETWEEN 0 AND 3),
    rating REAL CHECK(rating BETWEEN 0.0 AND 5.0),
    cuisine TEXT NOT NULL
);
""")

restaurants = [
    ("вул. Хрещатик, 15, Київ", 1, 4.7, "українська"),
    ("Via Roma 22, Рим, Італія", 2, 4.9, "італійська"),
    ("5-7-1 Ginza, Токіо, Японія", 3, 5.0, "азіатська"),
    ("вул. Сумська, 45, Харків", 0, 4.3, "українська"),
    ("123 Orchard Rd, Сінгапур", 2, 4.8, "азіатська")
]

cursor.executemany("""
INSERT INTO restaurants (address, michelin_stars, rating, cuisine)
VALUES (?, ?, ?, ?);
""", restaurants)


conn.commit()


cursor.execute("SELECT * FROM restaurants;")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
