import sqlite3
import requests
import time
from bs4 import BeautifulSoup

# Function to load all meets from the database
def read_meets():
    # Connect to the SQLite database
    conn = sqlite3.connect('track_meet_simulator.db')
    cursor = conn.cursor()

    # Query to get all the meets from the 'meets' table
    cursor.execute('SELECT * FROM meets')
    rows = cursor.fetchall()

    # List to store the meet details
    meets = []

    # Iterate through the rows and store the meet data
    for row in rows:
        meet_data = {
            'id': row[0],         # Meet ID
            'name': row[1],       # Meet name
            'link': row[2],       # Meet link
            'year': row[3],       # Meet year
            'outdoor': row[4]     # Outdoor (True/False)
        }
        meets.append(meet_data)

    # Close the database connection
    conn.close()

    return meets

# Function to check if results for a specific meet_id already exist in the 'meet_results' table
def results_exist_for_meet(meet_id):
    conn = sqlite3.connect('track_meet_simulator.db')
    cursor = conn.cursor()

    # Query to check if results already exist for the given meet_id
    cursor.execute('SELECT COUNT(*) FROM meet_results WHERE meet_id = ?', (meet_id,))
    result_count = cursor.fetchone()[0]

    conn.close()

    return result_count > 0  # If count is greater than 0, results exist

# Function to insert team results into the 'meet_results' table
def insert_meet_results(meet_id, team_name, points, place):
    conn = sqlite3.connect('track_meet_simulator.db')
    cursor = conn.cursor()

    # Insert the team result into the 'meet_results' table
    cursor.execute('''
        INSERT INTO meet_results (meet_id, team_name, points, place)
        VALUES (?, ?, ?, ?)
    ''', (meet_id, team_name, points, place))

    conn.commit()
    conn.close()

# Function to fetch results from a meet and store them
def fetch_results_from_meet(meets):

    for meet in meets:
        # Check if results for this meet already exist, if so, skip it
        if results_exist_for_meet(meet['id']):
            print(f"Skipping meet: {meet['name']} (ID: {meet['id']}), results already exist.")
            continue  # Skip to the next meet

        link = meet['link']

        # Fetch the results page for the meet
        results_page = requests.get(link)

        # Parse the page content using BeautifulSoup
        results_soup = BeautifulSoup(results_page.content, 'html.parser')

        # Print the link to ensure it's being fetched correctly
        print(link)

        # Find the table containing the results (use the correct table ID or class)
        table = results_soup.find('table', {'id': 'team_scores_m'})
        if not table:
            print(f"No results table found for {meet['name']}")
            continue

        # Find all rows in the table body
        rows = table.find('tbody').find_all('tr')

        for row in rows:
            # Extract the place, team name, and points
            tds = row.find_all('td')

            if len(tds) < 3:
                continue  # Ensure there are enough columns in the row

            place = int(tds[0].get_text().strip())        # Team's place (rank)
            team_name = tds[1].get_text().strip()         # Team's name
            points = float(tds[2].get_text().strip())     # Team's points

            # Print the extracted information for testing
            print(f"Place: {place}, Team: {team_name}, Points: {points}")

            # Insert the result into the database
            insert_meet_results(meet['id'], team_name, points, place)

        time.sleep(1.5)  # Sleep to avoid overloading the server with requests

def main():
    # Load the meets from the database
    meets = read_meets()

    # Fetch and store the results for each meet
    fetch_results_from_meet(meets)

if __name__ == "__main__":
    main()