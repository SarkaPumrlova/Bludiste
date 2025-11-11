import sqlite3

def save_top_time(player_name, final_time):
    conn = sqlite3.connect("game_data.db")
    cursor = conn.cursor()

    # Make sure table exists
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS top_times (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_name TEXT NOT NULL,
        time REAL NOT NULL,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Insert the player’s time
    cursor.execute("INSERT INTO top_times (player_name, time) VALUES (?, ?)", (player_name, final_time))

    conn.commit()
    conn.close()
