import os
import requests
import sqlite3
import time
from datetime import datetime

DB_NAME = "/opt/airflow/data/comics_xkcd.db"


# Create the comics_staging_data table if it doesn't exist
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comics_staging_data (
            comic_id INTEGER PRIMARY KEY,
            month TEXT,
            link TEXT,
            year TEXT,
            news TEXT,
            safe_title TEXT,
            transcript TEXT,
            alt TEXT,
            img TEXT,
            title TEXT,
            day TEXT,
            created_at DATETIME,
            updated_at DATETIME
        );
    """)
    conn.commit()
    conn.close()


# Check DB and table, return last comic_id (0 if starting fresh)
def check_table_status():
    if not os.path.exists(DB_NAME):
        print("Database file not found. Creating new one.")
        init_db()
        return 0

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Check if table exists
    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name='comics_staging_data';
    """)
    table_exists = cursor.fetchone()

    if not table_exists:
        print("Table not found. Creating comics_staging_data.")
        init_db()
        conn.close()
        return 0

    # Table exists, fetch max comic_id
    cursor.execute("SELECT MAX(comic_id) FROM comics_staging_data;")
    result = cursor.fetchone()
    conn.close()
    return result[0] if result and result[0] else 0


# Get the latest comic ID from the XKCD API
def get_latest_comic_id():
    try:
        response = requests.get("https://xkcd.com/info.0.json", timeout=3)
        response.raise_for_status()
        return response.json()["num"]
    except Exception as e:
        print(f"Error fetching latest comic ID: {e}")
        return None


# Fetch individual comic JSON
def fetch_xkcd_comic(comic_id):
    url = f"https://xkcd.com/{comic_id}/info.0.json"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 404:
            print(f"{comic_id} not found..")
            return None
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        print(f"Timeout occurred for {comic_id}. Skipping entry.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error occurred for {comic_id}: {e}. Skipping entry.")
        return None


# Insert comic record into the DB
def insert_xkcd_comic(data):
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO comics_staging_data (
            comic_id, month, link, year, news, safe_title,
            transcript, alt, img, title, day, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        data["num"],
        data.get("month", ""),
        data.get("link", ""),
        data.get("year", ""),
        data.get("news", ""),
        data.get("safe_title", ""),
        data.get("transcript", ""),
        data.get("alt", ""),
        data.get("img", ""),
        data.get("title", ""),
        data.get("day", ""),
        now,
        now
    ))
    conn.commit()
    conn.close()


print(DB_NAME)
