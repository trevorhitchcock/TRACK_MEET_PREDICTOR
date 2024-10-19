import sqlite3

def setup_database():
    # Connect to (or create) the SQLite database
    conn = sqlite3.connect('track_meet_simulator.db')
    cursor = conn.cursor()

    # Create the 'meets' table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS meets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            link TEXT NOT NULL,
            year INTEGER NOT NULL, -- stores year as an integer (YY)
            outdoor BOOL NOT NULL -- True if outdoor meet, False if indoor meet
        )
    ''')

    # Commit and close the connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    setup_database()
    print("Database and tables created successfully!")
