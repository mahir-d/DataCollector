''' This file Contains functions related to all functions related to Challenge '''
import requests
from requests.exceptions import HTTPError
import os
import json
from progress.bar import Bar
from process import format_challenge


def get_data(total_pages: int, total_challenges: int, params, start_date_start_range, end_date_start_range, storage_directory):
    ''' Fetches the API, formats and stores as JSON in given directory '''

    directory_name: str = f'challengeData_{start_date_start_range.date()}_{end_date_start_range.date()}'
    curr_dir = os.path.join(storage_directory,
                            directory_name)

    try:
        os.mkdir(curr_dir)
    except Exception as e:
        print("--- Directory exists ---", e)

    for i in range(1, int(total_pages) + 1):
        params['page'] = i

        response = requests.get(
            'http://api.topcoder.com/v5/challenges/', params=params,
            timeout=2.00)

        if response.ok:
            challenge_list = response.json()

            my_file = open(os.path.join(
                curr_dir, f'page {i}.json'), "w")
            with my_file:
                bar = Bar('Processing', max=params["perPage"])
                for challenge in challenge_list:
                    formatted_challenge = format_challenge(challenge)
                    json.dump(formatted_challenge, my_file, indent=4)
                    bar.next()

                bar.finish()
                my_file.close()
        print('Downloaded and store data from page {i}')
    print('All data downloaded')


def fetch_challenge_registrants(challenge_id: str):
    ''' Gets a list of all registrants for the challenge '''
    # Can add an env variable instead of static url
    member_url: str = f'https://api.topcoder.com/v5/resources?challengeId={challenge_id}'

    try:
        response = requests.get(member_url)

        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(
            f'HTTP error occurred: {http_err} on challengeId - {challenge_id} while fetching registrants')
    except Exception as err:
        # Python 3.6
        print(
            f'Other error occurred: {err} on challengeId - {challenge_id} while fetching registrants')
    else:
        return response.json()


def fetch_challenge_submissions(challenge_id: str):
    ''' Gets a list of all members who made a submission to the challenge '''
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1rWTNNamsxTWpNeU5Ua3dRalkzTmtKR00wRkZPRVl3TmtJd1FqRXlNVUk0TUVFNE9UQkZOZyJ9.eyJodHRwczovL3RvcGNvZGVyLmNvbS91c2VySWQiOiI5MDA2NDgwNCIsImh0dHBzOi8vdG9wY29kZXIuY29tL2hhbmRsZSI6Im1haGlyX3p6eiIsImh0dHBzOi8vdG9wY29kZXIuY29tL3JvbGVzIjpbIlRvcGNvZGVyIFVzZXIiXSwiaHR0cHM6Ly90b3Bjb2Rlci5jb20vdXNlcl9pZCI6ImF1dGgwfDkwMDY0ODA0IiwiaHR0cHM6Ly90b3Bjb2Rlci5jb20vdGNzc28iOiI5MDA2NDgwNHxjYzU1MjNlNzdlNzY2ODgwMjI5NjYxNzIxNTg3MGIxYTAzYzMwY2IxOWY0ODFiN2IyNzg5MGNlYWJmMDUxYiIsImh0dHBzOi8vdG9wY29kZXIuY29tL2FjdGl2ZSI6dHJ1ZSwibmlja25hbWUiOiJtYWhpcl96enoiLCJuYW1lIjoibWFoaXJkaGFsbDVAZ21haWwuY29tIiwicGljdHVyZSI6Imh0dHBzOi8vcy5ncmF2YXRhci5jb20vYXZhdGFyL2U1MDgxMjViZGNiZmM3YWU3NjMyZTQ0OGExNmZjMjU2P3M9NDgwJnI9cGcmZD1odHRwcyUzQSUyRiUyRmNkbi5hdXRoMC5jb20lMkZhdmF0YXJzJTJGbWEucG5nIiwidXBkYXRlZF9hdCI6IjIwMjEtMDItMTBUMDA6MzE6MjAuNzExWiIsImVtYWlsIjoibWFoaXJkaGFsbDVAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImlzcyI6Imh0dHBzOi8vYXV0aC50b3Bjb2Rlci5jb20vIiwic3ViIjoiYXV0aDB8OTAwNjQ4MDQiLCJhdWQiOiJVVzdCaHNubUFRaDBpdGw1NmcxalVQaXNCTzlHb293RCIsImlhdCI6MTYxMjkxNzA4MSwiZXhwIjoxNjEzMDAzNDgxLCJub25jZSI6Ik1UZEZWV0pLVUVWdWQxZFpaRTQwVjFjNU0xZHZTM05vV1RoSVZqTlBkRE0xZVRoblpVODJUbEkwZFE9PSJ9.FwKSkKsTopnr0mcDfkXSi6b62Ab5zuNaemSL_APJ1tgxTq3rrNgBMAJA_EP2TcRHAP2-353w_kvdytyFVnSUnTEuV__iALDQcTZTyELJij_d5eIagiD6YeoFGLLEby4xPqjSrl0aFi9ojDNVcQRUmaXTsAen7WnUki7pabfhvtDl7_nOOto8Z1t_q6stXtOYz04m3PMUzD57XPKkKu4iNelm4mZ2gBSepqbqnz3YuGlfInp8KDSldcc7-hycrGrB5JH8q5IUby9Vu4cz1sIN6sJ1YJOAmZOmI-UTmN53Fjq_7Pns1Ca0zxBavbWZESvJzQIFM2s34XueBYSOSCckYw'
    }

    url = f'https://api.topcoder.com/v5/submissions?challengeId={challenge_id}'
    try:
        response = requests.get(url, headers=headers)

        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(
            f'HTTP error occurred: {http_err} on challengeId - {challenge_id} while fetching registrants')
    except Exception as err:
        # Python 3.6
        print(
            f'Other error occurred: {err} on challengeId - {challenge_id} while fetching registrants')
    else:
        return response.json()


fetch_challenge_submissions("9af951b1-a60a-41b3-b350-41e4700e86c1")
