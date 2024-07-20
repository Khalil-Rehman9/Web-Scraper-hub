#!/usr/bin/python

import requests
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import Error
import json
from time import sleep
from random import randint

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
            cursor.execute("SELECT id,bolddk_match_id,parsed_match_date_time FROM `sports_footballmatch` WHERE parsed_match_date_time < NOW() - INTERVAL 1 HOUR AND status_type IS NULL ORDER BY id DESC;")
            matches = cursor.fetchall()
            # crawl each pening match
            for match in matches:
                sleep(randint(1,6))
                # get the match details from bold.dk API
                match_row_id = match[0]
                bolddk_match_id = match[1]
                api_url = 'https://api.bold.dk/stats/v1/matches/' + str(bolddk_match_id) + '/details'
                response = requests.get(api_url)
                if response.status_code == 200:
                    # store the match details in database
                    match_details = response.json()
                    try:
                        status_type = match_details['data'][0]['status_type']
                    except:
                        status_type = None
                    try:
                        status_short = match_details['data'][0]['status_short']
                    except:
                        status_short = None 
                    try:
                        status_long = match_details['data'][0]['status_long']
                    except:
                        status_long = None 
                    try:
                        round = match_details['data'][0]['round']
                    except:
                        round = None 
                    try:
                        scores = str(match_details['data'][0]['home_team']['score']) + " - " + str(match_details['data'][0]['away_team']['score'])
                        round = match_details['data'][0]['round']
                    except:
                        scores = None
                        round = None 
                    match_details_json = response.text
                    sql = """UPDATE sports_footballmatch 
                    SET
                    `status_type` = %s,
                    `status_short` = %s,
                    `status_long` = %s,
                    `scores` = %s,
                    `round` = %s
                    WHERE id = %s """
                    cursor.execute(sql,(status_type,status_short, status_long, scores, round, match_row_id))
                    connection.commit()
                    print(str(match_row_id)+' -done')
                # break

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
