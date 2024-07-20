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
            cursor.execute("SELECT id,bolddk_match_id,match_details_json,league FROM `sports_footballmatch`")
            matches = cursor.fetchall()
            # crawl each pening match
            for match in matches:
                # get the match details from bold.dk API
                match_details = json.loads(match[2])
                match_row_id = match[0]
                bolddk_match_id = match[1]
                api_url = 'https://api.bold.dk/stats/v1/matches/' + str(bolddk_match_id) + '/details'
                # api_url = 'http://localhost/test_json.json'
                # api_url = 'https://www.youtube.com'
                # response = requests.get(api_url)
                try:
                    league_country = match_details['data'][0]['tournament']['country']['name']
                except:
                    league_country = None
                sql = """UPDATE sports_footballmatch 
                SET  
                `league_country` = %s
                WHERE id = %s """
                cursor.execute(sql,(league_country, match_row_id))
                connection.commit()
                print(match_row_id)

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

