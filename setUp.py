''' This file '''
import sys
import requests
import json
from progress.bar import Bar
import os
from dbConnect import dbConnect
from fetch_functions import get_data


class setUp:
    ''' This class sets up the data calls based on the config provided'''

    def __init__(self, argsParsedData):
        # print(argsParsedData)
        self.storage_directory = argsParsedData.Path
        # self.storage_directory = "/Users/mahirdhall/Desktop/WebScrapping"
        self.start_date_start_range = argsParsedData.Start_date
        self.end_date_start_range = argsParsedData.End_date
        self.status = argsParsedData.Status
        self.sortedOrder = argsParsedData.SortedOrder
        self.track = argsParsedData.track
        self.params = {
            'page': 1,
            'perPage': 50,
            'status': self.status,
            'tracks[]': [self.track],
            'sortBy': 'startDate',
            'startDateStart': self.start_date_start_range.isoformat(),
            'startDateEnd': self.end_date_start_range.isoformat(),
            'sortOrder': self.sortedOrder
        }

    def request_info(self):
        ''' This fuction displays the available data on the provided config '''

        params = self.params

        response = requests.get(
            'http://api.topcoder.com/v5/challenges/', params=params,
            timeout=2.00)
        challenge_list = response.json()

        directory_path = self.storage_directory

        my_file = open(os.path.join(directory_path, f'demoData.json'), "w")
        # Loads sample data to demoData.json
        with my_file:
            bar = Bar('Processing', max=params["perPage"])
            for challenge in challenge_list:
                # print(challenge)
                json.dump(challenge, my_file, indent=4)
                bar.next()

            bar.finish()
            my_file.close()

        print(
            f'--- Sample data loaded to demoData.json at the path {directory_path} ---')

        total_pages = response.headers["X-Total-Pages"]
        total_challenges = response.headers["X-Total"]
        print(
            f'Do you want to go ahead and download {total_challenges} challenges? [y/n]?')
        ans: str = input()

        if ans == 'y':
            print('The download will begin now')
            get_data(total_pages, total_challenges, self.params,
                     self.start_date_start_range, self.end_date_start_range, self.storage_directory)
        else:
            print('Program terminated')
            sys.exit()


# This store directly to DB
    # def get_data(self, total_pages: int, total_challenges: int):
    #     ''' This function downloads all the data based on the given config '''

    #     params = self.params
    #     # Database config can be added here
    #     db_Config = {
    #         "username": "root",
    #         "hostname": "localhost",
    #         "password": "password",
    #         "port": "3306",
    #         "database": "dataCollector",
    #         "table_name": "Challenges"
    #     }

    #     try:
    #         print('connecting database')
    #         my_db = dbConnect(db_Config)
    #         print(' database connected')
    #         bar = Bar('Processing', max=int(total_pages))
    #         for i in range(1, int(total_pages) + 1):
    #             params['page'] = i

    #             response = requests.get(
    #                 'http://api.topcoder.com/v5/challenges/', params=params,
    #                 timeout=2.00)

    #             if response.ok:
    #                 challenge_list = response.json()
    #                 my_db.upload_data(challenge_list, "Challenges")

    #                 print('Downloaded and store data from page {i}')
    #             else:
    #                 print('Could not download data from page {i}')
    #             bar.next()
    #         bar.finish()
    #         print('All data downloaded')
    #     except Exception as e:
    #         print('hello')
    #         print(e)
