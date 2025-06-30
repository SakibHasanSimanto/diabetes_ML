# model/database.py

import sqlite3
import os

# Database file path
DB_PATH = os.path.join(os.path.dirname(__file__), '../prediction_history.db')

def create_table():
    """Creates the table if it doesn't exist"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input_data TEXT NOT NULL,
            result TEXT NOT NULL,
            probability REAL NOT NULL,
            risk_band TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def insert_prediction(input_data, result, probability, risk_band):
    """Inserts a new prediction record"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO predictions (input_data, result, probability, risk_band)
        VALUES (?, ?, ?, ?)
    ''', (str(input_data), result, probability, risk_band))
    conn.commit()
    conn.close()

def get_all_predictions():
    """Fetches all prediction records"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM predictions ORDER BY timestamp DESC')
    rows = cursor.fetchall()
    conn.close()
    return rows

def clear_history():
    """Deletes all records from the predictions table"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM predictions')
    conn.commit()
    conn.close()
