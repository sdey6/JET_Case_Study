"""
Helper script for DB creation, checking max comic number in DB, fetching latest comic from API
"""

import os
import requests
import sqlite3
import time
from datetime import datetime
from bs4 import BeautifulSoup
import re

DB_NAME = "/opt/airflow/data/comics_xkcd.db"


# Create comics_staging_data table if it doesnt exist
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
            updated_at DATETIME,
            title_cleaned TEXT,
            title_letter_count INTEGER
        );
    """)
    conn.commit()
    conn.close()


# check DB and table return last comic_id  and 0 if starting afresh
def check_table_status():
    if not os.path.exists(DB_NAME):
        print("Database file not found. Creating new one.")
        init_db()
        return 0

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # check if table exists
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

    # table exists and fetch max comic_id
    cursor.execute("SELECT MAX(comic_id) FROM comics_staging_data;")
    result = cursor.fetchone()
    conn.close()
    return result[0] if result and result[0] else 0


# Get the latest comic id from XKCD API
def get_latest_comic_id():
    try:
        response = requests.get("https://xkcd.com/info.0.json", timeout=3)
        response.raise_for_status()
        return response.json()["num"]
    except Exception as e:
        print(f"Error fetching latest comic ID: {e}")
        return None


# Fetch comic JSON
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


# Insert comic in the DB
def insert_xkcd_comic(data):
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    raw_title = data.get("title", "")
    title_cleaned = strip_html_tags(raw_title)  # removing html tags
    title_letter_count = count_alphabetic_letters(title_cleaned)  # calculate no of letters
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO comics_staging_data (
            comic_id, month, link, year, news, safe_title,
            transcript, alt, img, title, day, created_at, updated_at, title_cleaned, title_letter_count
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
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
        now,
        title_cleaned,
        title_letter_count
    ))
    conn.commit()
    conn.close()


# strip out html tags
def strip_html_tags(text):
    return BeautifulSoup(text, "html.parser").get_text()


# consider only alphabets
def count_alphabetic_letters(text):
    return len([char for char in text if char.isalpha()])

