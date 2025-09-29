import sqlite3
import json

DB_PATH = "vending_machine.db"

def get_conn():
    return sqlite3.connect(DB_PATH)

# --- Product CRUD ---
def get_products():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price, stock FROM products")
    products = cursor.fetchall()
    conn.close()
    return products

def update_product_stocks(product_id, new_stock):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET stock=? WHERE id=?", (new_stock, product_id))
    conn.commit()
    conn.close()

# --- Coin CRUD ---
def get_coin_stock():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT denomination, count FROM coin_stock")
    coins = dict(cursor.fetchall())
    conn.close()
    return coins

def update_coin_stock(coin, count):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("UPDATE coin_stock SET count=? WHERE denomination=?", (count, coin))
    conn.commit()
    conn.close()

# --- Transactions ---
def log_transaction(product_id, amount_paid, change):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO transactions (product_id, amount_paid, change_given) VALUES (?, ?, ?)",
        (product_id, amount_paid, json.dumps(change))
    )
    conn.commit()
    conn.close()
