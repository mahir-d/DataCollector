import datetime
import argparse

''' This file stores all the utility methods '''

'''
    Refernce to below code
    https://stackoverflow.com/questions/25470844/specify-format-for-input-arguments-argparse-python
'''


def valid_date(s):
    ''' Converts string input to datetime object '''
    try:
        return datetime.datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)
