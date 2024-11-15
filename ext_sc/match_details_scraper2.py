#!/usr/bin/python

import requests
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import Error
import json

if __name__ == "__main__":
    # get the matches, those not crawled yet
    try:
        # connection = mysql.connector.connect(host='localhost',
        #                                      database='webixhub',
        #                                      user='root',
        #                                      password='q1122')
        connection = mysql.connector.connect(host='localhost',
                                             database='webixhub',
                                             user='webixhub',
                                             password='9TNg6ICfEKWOowh7')
        if connection.is_connected():
            print('connected')
            db_Info = connection.get_server_info()
            cursor = connection.cursor()
            cursor.execute("SELECT id,bolddk_match_id FROM `sports_footballmatch` WHERE parsed_match_date_time > NOW() OR parsed_match_date_time IS NULL")
            matches = cursor.fetchall()
            # crawl each pening match
            for match in matches:
                # get the match details from bold.dk API
                match_row_id = match[0]
                bolddk_match_id = match[1]
                api_url = 'https://api.bold.dk/stats/v1/matches/' + \
                    str(bolddk_match_id) + '/details'
                response = requests.get(api_url)
                if response.status_code == 200:
                    # store the match details in database
                    match_details = response.json()
                    try:
                        home_team_id = match_details['data'][0]['home_team']['slug']
                    except:
                        home_team_id = None
                    try:
                        match_date = match_details['data'][0]['dates']['date']
                        match_time = match_date.split(" ")[1]
                    except:
                        match_date = None
                        match_time = None
                    try:
                        away_team_id = match_details['data'][0]['away_team']['slug']
                    except:
                        away_team_id = None
                    try:
                        league_id = match_details['data'][0]['tournament']['pretty_url']
                    except:
                        league_id = None
                    try:
                        league_country = match_details['data'][0]['tournament']['country']['name']
                    except:
                        league_country = None
                    match_details_json = response.text
                    sql = """UPDATE sports_footballmatch 
                    SET  
                    `is_match_details_crawled` = 1,
                    `league_id` = %s,
                    `home_team_id` = %s,
                    `away_team_id` = %s,
                    `match_details_json` = %s,
                    `league_country` = %s
                    WHERE id = %s """
                    cursor.execute(sql, (league_id, home_team_id, away_team_id,
                                   match_details_json, league_country, match_row_id))
                    connection.commit()
                    print(str(match_row_id)+' -done')
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

