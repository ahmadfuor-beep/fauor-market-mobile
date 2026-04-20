import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "fauor.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price REAL,
        category TEXT,
        image TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cart (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price REAL
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        city TEXT NOT NULL,
        home_location TEXT,
        phone TEXT NOT NULL,
        email TEXT,
        gender TEXT NOT NULL,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        total REAL NOT NULL,
        created_at TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        product_name TEXT NOT NULL,
        price REAL NOT NULL,
        FOREIGN KEY(order_id) REFERENCES orders(id)
    )
    """)

    conn.commit()
    conn.close()
    
 # insert products to DB if not already present
def insert_products(products):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM products")

    for p in products:
        cursor.execute("""
        INSERT INTO products (name, price, category, image)
        VALUES (?, ?, ?, ?)
        """, (p["name"], p["price"], p["category"], p["image"]))

    conn.commit()
    conn.close()
    
    # product retrieval
def get_products():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name, price, category, image FROM products")
    rows = cursor.fetchall()

    conn.close()

    return [
        {"name": r[0], "price": r[1], "category": r[2], "image": r[3]}
        for r in rows
    ]
    
    # cart management
def add_to_cart_db(product):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO cart (name, price)
    VALUES (?, ?)
    """, (product["name"], product["price"]))

    conn.commit()
    conn.close()


def get_cart_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, price FROM cart")
    rows = cursor.fetchall()

    conn.close()

    return [
{"id": r[0], "name": r[1], "price": r[2]}
        for r in rows
    ]

def remove_from_cart_db(item_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM cart WHERE id = ?", (item_id,))

    conn.commit()
    conn.close()

def clear_cart_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM cart")

    conn.commit()
    conn.close()
    
def create_user(first_name, last_name, city, home_location, phone, email, gender, username, password):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO users (
            first_name, last_name, city, home_location,
            phone, email, gender, username, password
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            first_name, last_name, city, home_location,
            phone, email, gender, username, password
        ))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def validate_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM users
    WHERE username = ? AND password = ?
    """, (username, password))

    user = cursor.fetchone()
    conn.close()

    return user is not None

# Fun to return user details
def get_user(username):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT first_name, last_name, city, home_location, phone, email, gender, username
    FROM users
    WHERE username = ?
    """, (username,))

    user = cursor.fetchone()
    conn.close()

    if user:
        return {
            "first_name": user[0],
            "last_name": user[1],
            "city": user[2],
            "home_location": user[3],
            "phone": user[4],
            "email": user[5],
            "gender": user[6],
            "username": user[7],
        }
    return None

# Fun to update user details
def update_user(username, first_name, last_name, city, home_location, phone, email, gender):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE users
    SET first_name = ?, last_name = ?, city = ?, home_location = ?,
        phone = ?, email = ?, gender = ?
    WHERE username = ?
    """, (
        first_name, last_name, city, home_location,
        phone, email, gender, username
    ))

    conn.commit()
    conn.close()
    
def create_order(username, cart_items):
    conn = get_connection()
    cursor = conn.cursor()

    total = sum(item["price"] for item in cart_items)
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO orders (username, total, created_at)
    VALUES (?, ?, ?)
    """, (username, total, created_at))

    order_id = cursor.lastrowid

    for item in cart_items:
        cursor.execute("""
        INSERT INTO order_items (order_id, product_name, price)
        VALUES (?, ?, ?)
        """, (order_id, item["name"], item["price"]))

    conn.commit()
    conn.close()
    
def get_orders_by_username(username):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, total, created_at
    FROM orders
    WHERE username = ?
    ORDER BY id DESC
    """, (username,))

    orders = cursor.fetchall()
    conn.close()

    return [
        {"id": row[0], "total": row[1], "created_at": row[2]}
        for row in orders
    ]
    
def get_order_items(order_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT product_name, price
    FROM order_items
    WHERE order_id = ?
    """, (order_id,))

    items = cursor.fetchall()
    conn.close()

    return [
        {"name": row[0], "price": row[1]}
        for row in items
    ]