"""
Simple SQLite database for CalTrack user data
"""
import sqlite3
import json
import hashlib
from datetime import datetime
from contextlib import contextmanager

DB_PATH = "caltrack.db"

@contextmanager
def get_db():
    """Context manager for database connections"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db():
    """Initialize database tables"""
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.execute("""
            CREATE TABLE IF NOT EXISTS meals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                food_description TEXT NOT NULL,
                calories INTEGER NOT NULL,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_meals_user_date 
            ON meals(user_id, date)
        """)

def hash_password(password):
    """Simple password hashing (use bcrypt in production)"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, password):
    """Create a new user"""
    try:
        with get_db() as conn:
            cursor = conn.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, hash_password(password))
            )
            return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None  # Username already exists

def authenticate_user(username, password):
    """Authenticate user and return user_id"""
    with get_db() as conn:
        user = conn.execute(
            "SELECT id FROM users WHERE username = ? AND password_hash = ?",
            (username, hash_password(password))
        ).fetchone()
        return user["id"] if user else None

def add_meal(user_id, date, food_description, calories, notes=""):
    """Add a meal for a user"""
    with get_db() as conn:
        cursor = conn.execute(
            """INSERT INTO meals (user_id, date, food_description, calories, notes)
               VALUES (?, ?, ?, ?, ?)""",
            (user_id, date, food_description, calories, notes)
        )
        return cursor.lastrowid

def get_meals_by_date(user_id, date):
    """Get all meals for a user on a specific date"""
    with get_db() as conn:
        meals = conn.execute(
            """SELECT id, food_description, calories, notes, created_at
               FROM meals WHERE user_id = ? AND date = ?
               ORDER BY created_at DESC""",
            (user_id, date)
        ).fetchall()
        return [dict(meal) for meal in meals]

def get_meals_by_month(user_id, year, month):
    """Get all meals for a user in a specific month"""
    date_pattern = f"{year}-{month:02d}-%"
    with get_db() as conn:
        meals = conn.execute(
            """SELECT date, SUM(calories) as total_calories
               FROM meals WHERE user_id = ? AND date LIKE ?
               GROUP BY date""",
            (user_id, date_pattern)
        ).fetchall()
        return {meal["date"]: meal["total_calories"] for meal in meals}

def delete_meal(user_id, meal_id):
    """Delete a meal"""
    with get_db() as conn:
        conn.execute(
            "DELETE FROM meals WHERE id = ? AND user_id = ?",
            (meal_id, user_id)
        )

def delete_meals_by_date(user_id, date):
    """Delete all meals for a user on a specific date"""
    with get_db() as conn:
        conn.execute(
            "DELETE FROM meals WHERE user_id = ? AND date = ?",
            (user_id, date)
        )

# Initialize database on import
init_db()
