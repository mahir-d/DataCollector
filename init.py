''' This file contains the command line interface or argument parser to set config of the
    data collector
'''
import argparse
import os
import sys
import datetime
from utility import valid_date
from setUp import setUp


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

    parser.add_argument('-st', '--status', dest='Status',
                        choices=['New', 'Draft', 'Cancelled', 'Active',
                                 'Completed'],
                        default='Completed',
                        help="Please choose the status of the challenges\
                            to be fetched. Default set as Completed")

    parser.add_argument('-so', '--sortOrder', choices=['asc', 'desc'],
                        dest='SortedOrder',
                        default='asc',
                        help="Should the challenges be sorted in ascending or\
                            descending order. Deafult set as asc")
    parser.add_argument('-tr', '--track', choices=['Dev', 'DS', 'Des', 'QA'],
                        help="Provide a track from Dev, DS, DES, QA. by default DEV",
                        default="Dev"
                        )

    args = parser.parse_args()

    # checks if the start date is greater or equal to the year 2000
    if args.Start_date <= datetime.datetime(2000, 1, 1):
        msg = "Start date year cannot be less than 2000"
        raise argparse.ArgumentTypeError(msg)

    # checks if the end date is less than the current date
    if args.End_date > datetime.datetime.now():
        msg = "End date year cannot be more than current date"
        raise argparse.ArgumentTypeError(msg)

    # checks if the end date is greater than the start date
    if args.End_date < args.Start_date:
        msg = "Start date should be less than the end date"
        raise argparse.ArgumentTypeError(msg)

    input_path = args.Path

    # Checks if the directory exists
    if not os.path.isdir(input_path):
        print('Error: The path specified is not a directory')
        sys.exit()

    s = setUp(args)
    s.request_info()
