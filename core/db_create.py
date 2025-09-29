import sqlite3
import os

DB_PATH = "vending_machine.db"

# --- สร้างโฟลเดอร์โปรเจกต์ (optional) ---
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True) if os.path.dirname(DB_PATH) else None

# --- สร้าง DB และเชื่อมต่อ ---
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# --- สร้างตาราง products ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price INTEGER NOT NULL,
    stock INTEGER NOT NULL
)
""")

# --- สร้างตาราง coin_stock ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS coin_stock (
    denomination INTEGER PRIMARY KEY,
    count INTEGER NOT NULL
)
""")

# --- สร้างตาราง transactions ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    amount_paid INTEGER,
    change_given TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# --- เติมสินค้าเริ่มต้น ---
drinks = [
    ("Orange", 20, 5),
    ("Mineral Water", 10, 10),
    ("Red Herb Tea", 25, 5),
    ("Green Tea", 15, 5),
    ("Kiwi Juice", 30, 5),
    ("Mosi Tea ★", 50, 1)  # collectible item
]

cursor.executemany("INSERT INTO products (name, price, stock) VALUES (?, ?, ?)", drinks)

# --- เติมเหรียญเริ่มต้น ---
coins = [
    (10, 10),
    (5, 10),
    (1, 20),
]

cursor.executemany("INSERT INTO coin_stock (denomination, count) VALUES (?, ?)", coins)

conn.commit()
conn.close()

print("Database vending_machine.db พร้อมใช้งานแล้ว 🎉")
