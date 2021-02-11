''' This file contains methods to parse json objects into correct format '''

from typing import Any, Dict
from utility import parse_iso_dt, calculate_prizes


def format_challenge(challenge_obj):
    ''' Converts challenge_obj variables in correct required format '''
    new_obj = {}
    new_obj["challengeId"] = challenge_obj["id"]
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


def format_member(member_obj):
    new_obj: Dict[str,Any] = {}
    # 0 means true, 1 means false
    new_obj["userId"] = member_obj["userId"]
    new_obj["memberHandle"] = member_obj["handle"]
    
    new_obj["DEVELOP"] = 0
    if member_obj["DEVELOP"] and member_obj["DEVELOP"]["challenges"] > 1:
        new_obj["DEVELOP"] = 1

    new_obj["DESIGN"] = 0
    if member_obj["DESIGN"] and member_obj["DESIGN"]["challenges"] > 1:
        new_obj["DESIGN"] = 1
    
    new_obj["DATA_SCIENCE"] = 0
    if member_obj["DATA_SCIENCE"] and member_obj["DATA_SCIENCE"]["challenges"] > 1:
        new_obj["DATA_SCIENCE"] = 1

    new_obj["maxRating"] = member_obj["maxRating"]["rating"]

    new_obj["track"] = None
    if member_obj["maxRating"].get("track"):
        new_obj["track"] = member_obj["maxRating"]["track"]
    
    new_obj["subTrack"] = None
    if member_obj["maxRating"].get("subTrack"):
        new_obj["subTrack"] = member_obj["maxRating"]["subTrack"] 
    
    new_obj["registrations"] = member_obj["challenges"]
    new_obj["wins"] = member_obj["wins"]

    return new_obj

