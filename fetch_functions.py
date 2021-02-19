''' This file Contains functions related to fetching from Topcoder API '''
from typing import List
import requests
from requests.exceptions import HTTPError
import os
import json
from progress.bar import Bar
from process import format_challenge, format_member, format_member_skills


def get_data(total_pages: int, total_challenges: int, params, start_date_start_range, end_date_start_range, storage_directory):
    ''' Fetches the API, formats and stores as JSON in given directory '''

    directory_name: str = f'challengeData_{start_date_start_range}_{end_date_start_range}'
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
                curr_dir, f'page{i}.json'), "w")
            
            with my_file:
                bar = Bar('Processing', max=params["perPage"])
                processed_challenge = []
                for challenge in challenge_list:
                    processed_challenge.append(format_challenge(challenge))
                    bar.next()
                json.dump(processed_challenge, my_file, indent=4)
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
        member_registrant_date = response.json()
        registrant_list = []
        for member in member_registrant_date:
            registrant_list.append(member["memberHandle"])
        return registrant_list


def fetch_challenge_submissions(challenge_id: str):
    ''' Gets a list of all members who made a submission to the challenge '''
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1rWTNNamsxTWpNeU5Ua3dRalkzTmtKR00wRkZPRVl3TmtJd1FqRXlNVUk0TUVFNE9UQkZOZyJ9.eyJodHRwczovL3RvcGNvZGVyLmNvbS91c2VySWQiOiI5MDA2NDgwNCIsImh0dHBzOi8vdG9wY29kZXIuY29tL2hhbmRsZSI6Im1haGlyX3p6eiIsImh0dHBzOi8vdG9wY29kZXIuY29tL3JvbGVzIjpbIlRvcGNvZGVyIFVzZXIiXSwiaHR0cHM6Ly90b3Bjb2Rlci5jb20vdXNlcl9pZCI6ImF1dGgwfDkwMDY0ODA0IiwiaHR0cHM6Ly90b3Bjb2Rlci5jb20vdGNzc28iOiI5MDA2NDgwNHxjYzU1MjNlNzdlNzY2ODgwMjI5NjYxNzIxNTg3MGIxYTAzYzMwY2IxOWY0ODFiN2IyNzg5MGNlYWJmMDUxYiIsImh0dHBzOi8vdG9wY29kZXIuY29tL2FjdGl2ZSI6dHJ1ZSwibmlja25hbWUiOiJtYWhpcl96enoiLCJuYW1lIjoibWFoaXJkaGFsbDVAZ21haWwuY29tIiwicGljdHVyZSI6Imh0dHBzOi8vcy5ncmF2YXRhci5jb20vYXZhdGFyL2U1MDgxMjViZGNiZmM3YWU3NjMyZTQ0OGExNmZjMjU2P3M9NDgwJnI9cGcmZD1odHRwcyUzQSUyRiUyRmNkbi5hdXRoMC5jb20lMkZhdmF0YXJzJTJGbWEucG5nIiwidXBkYXRlZF9hdCI6IjIwMjEtMDItMThUMjE6Mzc6MTYuNTgyWiIsImVtYWlsIjoibWFoaXJkaGFsbDVAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImlzcyI6Imh0dHBzOi8vYXV0aC50b3Bjb2Rlci5jb20vIiwic3ViIjoiYXV0aDB8OTAwNjQ4MDQiLCJhdWQiOiJVVzdCaHNubUFRaDBpdGw1NmcxalVQaXNCTzlHb293RCIsImlhdCI6MTYxMzY4NDIzNywiZXhwIjoxNjEzNzcwNjM3LCJub25jZSI6IlVUYzJaMlpOWkdGMmJVcExlVEZYYkVWamEzSmhaWEl6YXpaS1RWUTBOelJJWkdrdFlUQlBZWEJCUXc9PSJ9.BIeGtSkwcpZ3Os7r10LhGG7pVoz_p7Qqd7ZlyJgMqXBRm7-63UtqP_ueTrKhR-cWcrZfHzseG_jG7OkI9oi6Dn3j_bhUWEokcizMXBVDgp0Ws2HBFs2D-5RjX3Nt8by0Qjl84Nqf6ooOU5BFQ3wukvjwpslMcbt2dv9xzevbWUkTnFDhKYSPIgmQtNRHUrn2sQQjWU0QLLO2X6rFjaEcqvBaZh5xx0ew0oHZbkAZQ1qxlHJq6nl4gIxKXRMnPBrTUxwkhbfC2SlW1V_ARJuCcRazuNgfPlwuVw2V_jMiHrW9zbjHxUgxhoc2QRiEzGbjyd5R_S5esDurdvD11S50OQ'
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
        member_submission_data = response.json()
        submission_set = set()
        for member in member_submission_data:
            submission_set.add(member["createdBy"])
        return submission_set


def fetch_member_data(member: str):
    ''' Fetches member data from the given memeberHandle '''
    member = member.lower()
    response = requests.get(
        f'https://api.topcoder.com/v5/members/{member}/stats',
        timeout=2.00)
    
    if response.ok:
        member_json = response.json()
        processed_member = format_member(member_json[0])
        return processed_member
    else:
        raise FileNotFoundError(f'Error: Could not download data for member {member}')



def fetch_member_skills(member:str):
    member = member.lower()
    response = requests.get(
        f'https://api.topcoder.com/v5/members/{member}/skills',
        timeout=2.00)
    if response.ok:
        member_skill_json = response.json()
        return format_member_skills(member_skill_json)
    else:
        print(f'Error: Could not download the Skill data for member {member}')

