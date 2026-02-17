# Create database

import sqlite3
import json
import os
import datetime

def create_tables():
    conn = sqlite3.connect("game_data.db")
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        created_at TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS levels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        difficulty TEXT,
        size_x INTEGER,
        size_y INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_id INTEGER NOT NULL,
        level_id INTEGER NOT NULL,
        time_seconds INTEGER NOT NULL,
        moves INTEGER,
        success BOOLEAN,
        played_at TIMESTAMP,
        FOREIGN KEY (player_id) REFERENCES players(id),
        FOREIGN KEY (level_id) REFERENCES levels(id)
    )
    """)

    conn.commit()
    
    # Load and insert maps from maps.json
    maps_file = os.path.join(os.path.dirname(__file__), "maps.json")
    if os.path.exists(maps_file):
        with open(maps_file, 'r') as f:
            maps_data = json.load(f)
        
        for index, map_data in enumerate(maps_data["maps"]):
            height = len(map_data)
            width = len(map_data[0]) if map_data else 0
            
            # Determine difficulty: if bigger than 9x10, it's medium, otherwise easy
            difficulty = "medium" if (height > 9 or width > 10) else "easy"
            
            cursor.execute("""
            INSERT OR IGNORE INTO levels (name, difficulty, size_x, size_y)
            VALUES (?, ?, ?, ?)
            """, (f"Level {index + 1}", difficulty, width, height))
        
        conn.commit()
    
    conn.close()


def get_or_create_player(username):
    """Get player ID or create new player"""
    conn = sqlite3.connect("game_data.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM players WHERE username = ?", (username,))
    result = cursor.fetchone()
    
    if result:
        player_id = result[0]
    else:
        cursor.execute("INSERT INTO players (username, created_at) VALUES (?, ?)", (username, datetime.datetime.now()))
        conn.commit()
        player_id = cursor.lastrowid
    
    conn.close()
    return player_id

def get_level_id(width, height):
    """Get level ID based on map dimensions"""
    conn = sqlite3.connect("game_data.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM levels WHERE size_x = ? AND size_y = ?", (width, height))
    result = cursor.fetchone()
    
    conn.close()
    return result[0] if result else None

def save_attempt(player_id, level_id, time_seconds, moves, success):
    """Save a game attempt"""
    conn = sqlite3.connect("game_data.db")
    cursor = conn.cursor()
    
    cursor.execute("""
    INSERT INTO attempts (player_id, level_id, time_seconds, moves, success, played_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (player_id, level_id, time_seconds, moves, success, datetime.datetime.now()))
    
    conn.commit()
    conn.close()

def save_top_time(player_name, final_time):
    conn = sqlite3.connect("game_data.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO top_times (player_name, time) VALUES (?, ?)", (player_name, final_time))

    conn.commit()
    conn.close()
