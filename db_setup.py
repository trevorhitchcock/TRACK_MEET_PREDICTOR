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
            year INTEGER NOT NULL,
            outdoor BOOL NOT NULL
        )
    ''')

    # Create the 'meet_results' table to store team results for each meet
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS meet_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meet_id INTEGER NOT NULL,  -- Foreign key linking to meets table
            team_name TEXT NOT NULL,
            points REAL NOT NULL,      -- Allow points to be a float (REAL)
            place INTEGER NOT NULL,
            FOREIGN KEY (meet_id) REFERENCES meets (id)  -- Linking results to specific meet
        )
    ''')

    # Commit and close the connection
    conn.commit()
    conn.close()

# Call the function to set up the database and tables
if __name__ == '__main__':
    setup_database()
    print("Database and tables created successfully!")
