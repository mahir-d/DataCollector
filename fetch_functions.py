''' This file Contains functions related to fetching from Topcoder API '''
from typing import List
import requests
from requests.exceptions import HTTPError
import os
import json
from progress.bar import Bar
from process import format_challenge, format_member, format_member_skills
from dotenv import load_dotenv


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
    load_dotenv()
    headers = {
        'Authorization': os.environ.get("authKey")
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
        print(response.status_code)
        raise FileNotFoundError(
            f'Error: Could not download data for member {member}')


def fetch_member_skills(member: str):
    member = member.lower()
    response = requests.get(
        f'https://api.topcoder.com/v5/members/{member}/skills',
        timeout=2.00)
    if response.ok:
        member_skill_json = response.json()
        return format_member_skills(member_skill_json)
    else:
        print(f'Error: Could not download the Skill data for member {member}')
