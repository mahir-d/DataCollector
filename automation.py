''' This file automates the process of downloading and uploading the data
    using the topcoder API
'''
from setUp import setUp
from uploader import Uploader
from datetime import datetime
from utility import valid_date
import argparse
import os


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
    
    ''' ---------------------------ArgParser starts here -----------------------'''

    parser = argparse.ArgumentParser(prog='init',
                                     usage='%(prog)s [options] path',
                                     description='Sets up the configuration\
                                        for the data fetcher',
                                     epilog="Made by Mahir Dhall"
                                     )

    parser.add_argument('Start_year',help="Please enter start year to fetch challenges and members from", type=int)
    
    parser.add_argument('End_year', help="Please enter end year to fetch challenges and members till inclusive", type=int)

    parser.add_argument('Status',
                        choices=['New', 'Draft', 'Cancelled', 'Active',
                                 'Completed'],
                        default='Completed',
                        help="Please choose the status of the challenges\
                            to be fetched. Default set as Completed")
    
    parser.add_argument('Path', metavar='path', type=str,
                        help="Path to the directory to store data")

    args = parser.parse_args()
    # Checks if the path to the directory is valid
    if not os.path.isdir(args.Path):
        msg = "Path should be a valid directory"
        raise argparse.ArgumentTypeError(msg)

    if args.Start_year <= 2000 or args.Start_year > 2050:
        msg = "Start_year should be greater than 2000"
        raise argparse.ArgumentTypeError(msg)

    if args.End_year <= 2000 or args.End_year > 2050:
        msg = "End_year should be greater than 2000"
        raise argparse.ArgumentTypeError(msg)
    
    if args.Start_year > args.End_year:
        msg = "Start_year should be less than End_year"
        raise argparse.ArgumentTypeError(msg)

    

    for year in range(args.Start_year, args.End_year + 1):
        A = Automation(
            year, args.Status, args.Path)
        A.fetch_challenges()

