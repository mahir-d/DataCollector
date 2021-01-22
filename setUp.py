''' This file '''
import sys
import requests
import json
from progress.bar import Bar
import os


class setUp:
    ''' This class sets up the data calls based on the config provided'''

    def __init__(self, argsParsedData):
        # print(argsParsedData)
        self.storage_directory = argsParsedData.Path
        self.start_date_start_range = argsParsedData.Start_date
        self.end_date_start_range = argsParsedData.End_date
        self.status = argsParsedData.Status
        self.sortedOrder = argsParsedData.SortedOrder
        self.params = {
            'page': 1,
            'perPage': 50,
            'status': self.status,
            'tracks[]': 'Dev',
            'sortBy': 'startDate',
            'startDateStart': self.start_date_start_range.isoformat(),
            'endDateEnd': self.end_date_start_range.isoformat(),
            'sortOrder': self.sortedOrder
        }

    def request_info(self):
        ''' This fuction displays the available data on the provided config '''

        params = self.params

        response = requests.get(
            'http://api.topcoder.com/v5/challenges/', params=params,
            timeout=2.00)
        challenge_list = response.json()

        director_path = self.storage_directory

        my_file = open(os.path.join(director_path, f'demoData.json'), "w")
        with my_file:
            bar = Bar('Processing', max=params["perPage"])
            for challenge in challenge_list:
                # print(challenge)
                json.dump(challenge, my_file, indent=4)
                bar.next()

            bar.finish()
            my_file.close()

        print('--- Sample data loaded to demoData.json at the directory path ---')

        total_pages = response.headers["X-Total-Pages"]
        total_challenges = response.headers["X-Total"]

        print(
            f'Total no of Pages - {total_pages}\
                with {params["perPage"]} challenges per Page')
        print(
            f'Total No of challenges - {total_challenges}\
                with status {params["status"]}')

        print(
            f'Do you want to go ahead and\
                download {total_challenges} challenges? [y/n]?')
        ans: str = input()

        if ans == 'y':
            print('The download will begin now')
            self.get_data(total_pages, total_challenges)
        else:
            print('Program terminated')
            sys.exit()

    def get_data(self, total_pages: int, total_challenges: int):
        ''' This function downloads all the data based on the given config '''

        params = self.params
        curr_dir = os.path.join(self.storage_directory,
                                f'data {self.start_date_start_range}')
        os.mkdir(curr_dir)

        for i in range(1, int(total_pages) + 1):
            params['page'] = i

            response = requests.get(
                'http://api.topcoder.com/v5/challenges/', params=params,
                timeout=2.00)

            if response.ok:
                challenge_list = response.json()
                director_path = self.storage_directory

                my_file = open(os.path.join(
                    curr_dir, f'page {i}.json'), "w")
                with my_file:
                    bar = Bar('Processing', max=params["perPage"])
                    for challenge in challenge_list:
                        # print(challenge)
                        json.dump(challenge, my_file, indent=4)
                        bar.next()

                    bar.finish()
                    my_file.close()
            print('Downloaded and store data from page {i}')
        print('All data downloaded')
