import sqlite3
import time

conn = sqlite3.connect("game.db", check_same_thread=False)
cur = conn.cursor()

def init_db():
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        cash INTEGER,
        last_collect INTEGER
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS city (
        user_id INTEGER PRIMARY KEY,
        name TEXT,
        population INTEGER,
        happiness INTEGER
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS buildings (
        user_id INTEGER PRIMARY KEY,
        houses INTEGER,
        school INTEGER,
        hospital INTEGER,
        police INTEGER
    )
    """)
    conn.commit()

def user_exists(uid):
    cur.execute("SELECT 1 FROM users WHERE user_id=?", (uid,))
    return cur.fetchone() is not None

def create_user(uid, city_name):
    now = int(time.time())
    cur.execute("INSERT INTO users VALUES (?,?,?)", (uid, 1000, now))
    cur.execute("INSERT INTO city VALUES (?,?,?,?)", (uid, city_name, 100, 80))
    cur.execute("INSERT INTO buildings VALUES (?,?,?,?,?)", (uid, 1, 0, 0, 0))
    conn.commit()

def get_user(uid):
    cur.execute("SELECT cash,last_collect FROM users WHERE user_id=?", (uid,))
    return cur.fetchone()

def get_city(uid):
    cur.execute("SELECT name,population,happiness FROM city WHERE user_id=?", (uid,))
    return cur.fetchone()

def get_buildings(uid):
    cur.execute("SELECT houses,school,hospital,police FROM buildings WHERE user_id=?", (uid,))
    return cur.fetchone()

def update_cash(uid, amount):
    cur.execute("UPDATE users SET cash=? WHERE user_id=?", amount)
    conn.commit()

def update_last_collect(uid, ts):
    cur.execute("UPDATE users SET last_collect=? WHERE user_id=?", (ts, uid))
    conn.commit()
