import os
import sqlite3

from bs4 import BeautifulSoup

def insert_meet_into_db(meet_name, meet_link, meet_year, meet_outdoor):
    conn = sqlite3.connect('track_meet_simulator.db')
    cursor = conn.cursor()

    # Insert the meet data into the 'meets' table
    cursor.execute('''
        INSERT INTO meets (name, link, year, outdoor)
        VALUES (?, ?, ?, ?)
    ''', (meet_name, meet_link, meet_year, meet_outdoor))

    conn.commit()
    conn.close()


def load_meets():
    
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # builds path to HTML file that consists of all conference meets
    file_path = os.path.join(current_dir, 'TFRRS_conference_meets.html')

    with open(file_path, 'r', encoding='utf-8') as file:
        
        tffrs_soup = BeautifulSoup(file, 'html.parser')
        
        # finds the tbody element by its id
        tbody = tffrs_soup.find('tbody', {'id': 'body'})
        
        # list to store data of all meets
        meets = []

        for row in tbody.find_all('tr'):
            # gets all <td> elements in the row
            tds = row.find_all('td')

            # check if last <td> contains 'Track & Field' to exclude Cross Country meets
            if tds and tds[-1].get_text().strip() == 'Track & Field':
                # <a> tag  contains the meet info
                meet_anchor = row.find('a')

                if meet_anchor:
                    # extracts meet name (text inside the <a> tag)
                    meet_name = meet_anchor.get_text().strip()
                    
                    # extracts link (href attribute of the <a> tag)
                    meet_link = meet_anchor['href']

                    # extracts date (in the second <td>)
                    meet_date_str = tds[1].get_text().strip()

                    meet_year = int(meet_date_str.split('/')[-1])

                    meet_outdoor = True

                    if 'indoor' in meet_name.lower():
                        meet_outdoor = False

                    # stores info
                    meet_info = {
                        'name': meet_name,
                        'link': meet_link,
                        'date': meet_year,
                        'outdoor' : meet_outdoor
                    }
                    
                    insert_meet_into_db(meet_name, meet_link, meet_year, meet_outdoor)
    print('done')
                    
load_meets()
