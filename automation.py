''' This file automates the process of downloading and uploading the data
    using the topcoder API
'''
from setUp import setUp
from uploader import Uploader
from datetime import datetime
from utility import valid_date
import time


class Automation:
    '''
        This class contains functions to fetch and upload challenge to database
    '''

    def __init__(self, year: int, status: str, storage_directory) -> None:
        self.year = year
        self.status = status
        # self.storage_directory =
        self.storage_directory = storage_directory

    def fetch_challenges(self):
        ''' Fetches challenge and memeber from the API and uploads the data 
            to the db
        '''
        for i in range(12):
            month = i + 1
            Start_date_end = ""
            Start_date_start = ""
            obj = {}
            if month == 12:
                Start_date_start = datetime(self.year, month, 2).date()
                Start_date_end = datetime(self.year, month, 31).date()
                print("Downloading data from -> ",
                      Start_date_start, " to ", Start_date_end)
                obj = {
                    "storage_directory": self.storage_directory,
                    "Start_date_start": Start_date_start,
                    "Start_date_end": Start_date_end,
                    "Status": self.status,
                    "SortedOrder": "asc",
                    "track": "Dev"
                }
            else:
                Start_date_start = datetime(self.year, month, 1).date()
                Start_date_end = datetime(self.year, month + 1, 1).date()
                print("Downloading data from -> ",
                      Start_date_start, " to ", Start_date_end)
                obj = {
                    "storage_directory": self.storage_directory,
                    "Start_date_start": Start_date_start,
                    "Start_date_end": Start_date_end,
                    "Status": self.status,
                    "SortedOrder": "asc",
                    "track": "Dev"
                }

            setup_obj = setUp(obj)
            setup_obj.request_info()
            up = Uploader(
                f'/Users/mahirdhall/Desktop/WebScrapping/challengeData_{Start_date_start}_{Start_date_end}')


if __name__ == '__main__':
    start = time.perf_counter()

    A = Automation(
        2020, "Cancelled", "/Users/mahirdhall/Desktop/WebScrapping")
    A.fetch_challenges()
    print(round(time.perf_counter() - start, 2))
