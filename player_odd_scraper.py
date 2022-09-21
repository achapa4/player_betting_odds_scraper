import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import os


# Make a list of the specific players you want to collect data for.
my_players = ['Justin Herbert', 'Alvin Kamara', 'Aaron Jones',  'James Robinson', 'Mark Ingram II', 'Breece Hall', 'Chris Godwin', 'Rashod Bateman',
              'Allen Lazard', 'Brandon Aiyuk', 'Hayden Hurst',]

# Create a function that Scrapes Rushing Yard Odds and returns a Pandas DataFrame
def rush_yds_odds(url, my_players):
    # Create an empty dictionary to store values
    rush_odds_df = {
        'player_name': [],
        'yard_estimate': [],
        'over_odds': [],
        'under_odds': [],
        'actual_yards': [],
        'yard_diff': []
    }
    # Make a request to the URL
    response = requests.get(url)
    # If status code OK, then start scraping website
    if response.status_code != 200:
        raise Exception("Error Loading Web Page")
    else:
        #Create a BeautifulSoup instance that returns html text document.
        doc = BeautifulSoup(response.text, 'html.parser')
        prop_div = doc.find_all('div', class_= 'sportsbook-event-accordion__wrapper expanded')
        # Loop through elements to find relevant data
        for index, prop in enumerate(prop_div):
            # If statement to ensure we are scraping the correct table
            if prop.a.text == 'Rush Yds':
                # Find the table with the data we need
                table = prop.find('tbody', class_='sportsbook-table__body')
                rows = table.find_all('tr')
                # Loop through rows
                for row in rows:
                    # If player name matches my_player list, scrape and parse data.
                    if row.th.text in my_players:
                        rush_odds_df['player_name'].append(row.th.text)
                        columns = row.find_all('td')
                        rush_odds_df['yard_estimate'].append(columns[0].text[:-4].split()[1])
                        rush_odds_df['over_odds'].append(columns[0].text[-4:])
                        rush_odds_df['under_odds'].append(columns[1].text[-4:])
                        rush_odds_df['actual_yards'].append(0)
                        rush_odds_df['yard_diff'].append(0)
                        
    return pd.DataFrame(rush_odds_df)
  
  
  # Function works the same as previous but for Receiving Yards.
def rec_yds_odds(url, my_players):
    rec_odds_df = {
        'player_name': [],
        'yard_estimate': [],
        'over_odds': [],
        'under_odds': [],
        'actual_yards': [],
        'yard_diff': []
    }
    
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Error Loading Web Page")
    else:
        doc = BeautifulSoup(response.text, 'html.parser')
        prop_div = doc.find_all('div', class_= 'sportsbook-event-accordion__wrapper expanded')
        for index, prop in enumerate(prop_div):
            if prop.a.text == 'Rec Yds':
                #print(prop.a.text)
                table = prop.find('tbody', class_='sportsbook-table__body')
                #print('------------------------------------')
                rows = table.find_all('tr')
                for row in rows:
                    if row.th.text in my_players:
                        #print(row.th.text)
                        rec_odds_df['player_name'].append(row.th.text)
                        columns = row.find_all('td')
                        #print(columns[0].text)
                        rec_odds_df['yard_estimate'].append(columns[0].text[:-4].split()[1])
                        #print(columns[0].text)
                        #print(columns[0].text[-4:])
                        rec_odds_df['over_odds'].append(columns[0].text[-4:])
                        rec_odds_df['under_odds'].append(columns[1].text[-4:])
                        rec_odds_df['actual_yards'].append(0)
                        rec_odds_df['yard_diff'].append(0)
                        
    return pd.DataFrame(rec_odds_df)
  
  
  # Saves a CSV file, if file already exists it appends data instead
def create_append_csv(file_path,dataframe):
    if os.path.exists(file_path):
        print("Master file already exists....")
        print("Appending to file instead...")
        master_file = pd.read_csv(file_path, index_col=[0])
        df_2 = dataframe
        master_file = master_file.append(df_2, ignore_index=True)
        master_file.to_csv(file_path)
    else:
        dataframe.to_csv(file_path)
