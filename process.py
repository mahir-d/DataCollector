''' This file contains methods to process json objects into correct format '''

from typing import Dict
from utility import parse_iso_dt, calculate_prizes


def format_challenge(challenge_obj):
    ''' Converts challenge_obj variables in correct required format '''
    new_obj = {}
    new_obj["challengeID"] = challenge_obj["id"]
    new_obj["legacyId"] = int(challenge_obj["legacyId"])
    new_obj["directProjectId"] = challenge_obj["legacy"]["directProjectId"]
    new_obj["status"] = challenge_obj["status"]
    new_obj["trackType"] = challenge_obj["track"]
    new_obj["type"] = challenge_obj["type"]
    new_obj["name"] = challenge_obj["name"]
    # can call a function to clean this format
    new_obj["description"] = challenge_obj["description"]
    new_obj["totalPrizes"] = calculate_prizes(challenge_obj["prizeSets"][0])
    new_obj["winners"] = ",".join([w["handle"]
                                   for w in challenge_obj["winners"]])
    new_obj["registrationStartDate"] = parse_iso_dt(
        challenge_obj["registrationStartDate"])
    new_obj["registrationEndDate"] = parse_iso_dt(
        challenge_obj["registrationEndDate"])
    new_obj["submissionStartDate"] = parse_iso_dt(
        challenge_obj["submissionStartDate"])
    new_obj["submissionEndDate"] = parse_iso_dt(
        challenge_obj["submissionEndDate"])
    new_obj["startDate"] = parse_iso_dt(challenge_obj["startDate"])
    new_obj["endDate"] = parse_iso_dt(challenge_obj["endDate"])
    new_obj["technologies"] = ",".join(challenge_obj["tags"])
    new_obj["numberOfSubmissions"] = challenge_obj["numOfSubmissions"]
    new_obj["numberOfRegistrants"] = challenge_obj["numOfRegistrants"]
    new_obj["forumId"] = challenge_obj["legacy"]["forumId"]

    return new_obj
