import sqlite3
import os

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