import sqlite3
import time

# ---------------- CONNECTION ----------------
conn = sqlite3.connect("game.db", check_same_thread=False)
cur = conn.cursor()

# ---------------- INIT ----------------
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

# ---------------- USERS ----------------
def user_exists(uid: int) -> bool:
    cur.execute("SELECT 1 FROM users WHERE user_id=?", (uid,))
    return cur.fetchone() is not None


def create_user(uid: int, city_name: str):
    now = int(time.time())

    cur.execute(
        "INSERT INTO users VALUES (?,?,?)",
        (uid, 1000, now)
    )

    cur.execute(
        "INSERT INTO city VALUES (?,?,?,?)",
        (uid, city_name, 100, 80)
    )

    cur.execute(
        "INSERT INTO buildings VALUES (?,?,?,?,?)",
        (uid, 1, 0, 0, 0)
    )

    conn.commit()


def get_user(uid: int):
    cur.execute(
        "SELECT cash, last_collect FROM users WHERE user_id=?",
        (uid,)
    )
    return cur.fetchone()


def update_cash(uid: int, cash: int):
    cur.execute(
        "UPDATE users SET cash=? WHERE user_id=?",
        (cash, uid)
    )
    conn.commit()


def update_last_collect(uid: int, ts: int):
    cur.execute(
        "UPDATE users SET last_collect=? WHERE user_id=?",
        (ts, uid)
    )
    conn.commit()

# ---------------- CITY ----------------
def get_city(uid: int):
    cur.execute(
        "SELECT name, population, happiness FROM city WHERE user_id=?",
        (uid,)
    )
    return cur.fetchone()


def update_city(uid: int, population: int, happiness: int):
    cur.execute(
        "UPDATE city SET population=?, happiness=? WHERE user_id=?",
        (population, happiness, uid)
    )
    conn.commit()

# ---------------- BUILDINGS ----------------
def get_buildings(uid: int):
    cur.execute(
        "SELECT houses, school, hospital, police FROM buildings WHERE user_id=?",
        (uid,)
    )
    return cur.fetchone()


def update_buildings(
    uid: int,
    houses: int,
    school: int,
    hospital: int,
    police: int
):
    cur.execute(
        """
        UPDATE buildings
        SET houses=?, school=?, hospital=?, police=?
        WHERE user_id=?
        """,
        (houses, school, hospital, police, uid)
    )
    conn.commit()
