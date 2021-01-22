
import argparse
import os
import sys
import datetime
from utility import valid_date


class setUp:

    def __init__(self, argsParsedData):
        # print(argsParsedData)
        self.storage_directory = argsParsedData.Path
        self.start_date_start_range = argsParsedData.Start_date
        self.end_date_start_range = argsParsedData.End_date


if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog='init',
                                     usage='%(prog)s [options] path',
                                     description='Sets up the configuration\
                                        for the data fetcher',
                                     epilog="Made by Mahir Dhall"
                                     )

    parser.add_argument('Path', metavar='path', type=str,
                        help="Path to the directory to store data")

    parser.add_argument('Start_date', metavar='start_date', type=valid_date,
                        help="Challenge start date - format YYYY-MM-DD")

    parser.add_argument('End_date', metavar='end_date', type=valid_date,
                        help="Challenge end date - format YYYY-MM-DD")

    parser.add_argument('-st', '--status',
                        choices=['New', 'Draft', 'Cancelled', 'Active',
                                 'Completed'],
                        help="Please choose the status of the challenges\
                            to be fetched")

    parser.add_argument('-so', '--sortOrder', choices=['asc', 'desc'],
                        default='asc',
                        help="Should the challenges be sorted in ascending or\
                            descending order")

    args = parser.parse_args()
    print(args)

    # Conditions check for given arguments
    if args.Start_date <= datetime.datetime(2000, 1, 1):
        msg = "Start date year cannot be less than 2000"
        raise argparse.ArgumentTypeError(msg)

    if args.End_date > datetime.datetime.now():
        msg = "End date year cannot be more than current date"
        raise argparse.ArgumentTypeError(msg)

    if args.End_date < args.Start_date:
        msg = "Start date should be less than the end date"
        raise argparse.ArgumentTypeError(msg)

    input_path = args.Path

    # if not os.path.isdir(input_path):
    #     print('Error: The path specified is not a directory')
    #     sys.exit()

    s = setUp(args)
