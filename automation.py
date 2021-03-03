from setUp import setUp
from uploader import Uploader
from datetime import datetime
from utility import valid_date
import time


class Automation:

    def __init__(self, year: int) -> None:

        self.year = year
        self.storage_directory = "/Users/mahirdhall/Desktop/WebScrapping"

    def fetch_challenges(self):

        for i in range(12):
            month = i + 1
            Start_date_end = ""
            Start_date_start = ""
            obj = {}
            if month == 12:
                Start_date_start = datetime(self.year, month, 2).date()
                Start_date_end = datetime(self.year, month, 31).date()
                print(Start_date_start, Start_date_end)
                obj = {
                    "storage_directory": self.storage_directory,
                    "Start_date_start": Start_date_start,
                    "Start_date_end": Start_date_end,
                    "Status": "Completed",
                    "SortedOrder": "asc",
                    "track": "Dev"
                }
            else:
                Start_date_start = datetime(self.year, month, 1).date()
                Start_date_end = datetime(self.year, month + 1, 1).date()
                print(Start_date_start, Start_date_end)
                obj = {
                    "storage_directory": self.storage_directory,
                    "Start_date_start": Start_date_start,
                    "Start_date_end": Start_date_end,
                    "Status": "Completed",
                    "SortedOrder": "asc",
                    "track": "Dev"
                }

            setup_obj = setUp(obj)
            setup_obj.request_info()
            up = Uploader(
                f'/Users/mahirdhall/Desktop/WebScrapping/challengeData_{Start_date_start}_{Start_date_end}')


if __name__ == '__main__':
    start = time.perf_counter()
    A = Automation(2020)
    A.fetch_challenges()
    print(round(time.perf_counter() - start, 2))
