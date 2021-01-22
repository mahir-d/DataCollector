import requests


class setUp:

    def __init__(self, argsParsedData):
        # print(argsParsedData)
        self.storage_directory = argsParsedData.Path
        self.start_date_start_range = argsParsedData.Start_date
        self.end_date_start_range = argsParsedData.End_date
        self.status = argsParsedData.Status
        self.sortedOrder = argsParsedData.SortedOrder

    def request_info(self):
        ''' This fuction displays the available data on the provided config '''
        params = {
            'page': 1,
            'perPage': 20,
            'status': self.status,
            'startDateStart': self.start_date_start_range,
            'endDateEnd': self.end_date_start_range,
            'sortOrder': self.sortedOrder
        }
        response = requests.get(
            'http://api.topcoder.com/v5/challenges/', params=params,
            timeout=2.00)

        print(response)

        print(response.headers)
