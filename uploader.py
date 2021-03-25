''' This file contains fuctions to upload processed data to database '''
import json
from os import listdir, getcwd, chdir
from os.path import isfile, join, isdir
from typing import Any, Dict, List, Set
from dbConnect import dbConnect
from fetch_functions import fetch_challenge_registrants, fetch_challenge_submissions, fetch_member_data, fetch_member_skills
from progress.bar import Bar


class Uploader:
    ''' Ths class contains functions to uplod data to the database '''

    def __init__(self, directory: str) -> None:
        self.db_config = {
            "username": "root",
            "hostname": "localhost",
            "password": "password",
            "port": "3306",
            "database": "dataCollector_v2",
            "table_name": "Challenges"
        }
        self.member_set: Set[str] = set()
        self.db_obj = dbConnect(self.db_config)
        self.storage_directory = directory
        # call the upload challenge function
        self.uploadChallenges(self.storage_directory)

        # Remove existing members from the set
        self.check_unique_members(self.member_set)
        # call the member upload function
        self.upload_members(self.member_set)

    # directory can be called in the constructor
    def uploadChallenges(self, directory):
        ''' Loads processed challenge from json file and upload it to DB while 
            fetching registrants and submissions from the API
        '''
        if not isdir(directory):
            raise NotADirectoryError(f'{directory} is not a valid directory')

        file_list = [file for file in listdir(
            directory) if file.endswith('.json')]

        if file_list:
            chdir(directory)
            for file_name in file_list:
                try:
                    file_location = join(directory, file_name)
                    curr_json_file = open(file_location, "r")
                except OSError as exception:
                    print(exception)
                    print(f'File {file_name} could not be opened')
                else:
                    json_data = curr_json_file.read()
                    challenge_json = json.loads(json_data)

                    challenge_progress = Bar(
                        "Uploading Challenges", max=len(challenge_json))
                    for challenge in challenge_json:
                        challenge_primary_id: int = self.db_obj.upload_data(
                            challenge, "Challenges")
                        if challenge_primary_id != -1:
                            self.load_challenge_members(
                                challenge, challenge["winners"], challenge_primary_id)
                        challenge_progress.next()
                    challenge_progress.finish()
                    print(
                        f'Finished loading challenges and all its members from {file_name}')

        else:
            print(f'No JSON files found in {directory}')

    def load_challenge_members(self, challenge: Dict[str, Any], challenge_winner: List[str], challenge_primary_id: int):
        ''' Fetches all registrants, submissions and winners, loads it to the mapping 
            database based on challenge_id and challenge_winner
        '''
        winners_list = challenge_winner.split(",")
        winner_dict: Dict[str, int] = {}
        for position, winner in enumerate(winners_list):
            winner_dict[winner] = position + 1

        submission_set: Set[str] = fetch_challenge_submissions(
            challenge["challengeId"])
        registrants_list: List[str] = fetch_challenge_registrants(
            challenge["challengeId"])

        if registrants_list:
            for members in registrants_list:
                # append members to a list for future use
                self.member_set.add(members)
                new_member_obj = {
                    "id": challenge_primary_id,
                    "challengeId": challenge["challengeId"],
                    "legacyId": challenge["legacyId"],
                    "memberHandle": members,
                    "submission": 1 if submission_set and members in submission_set else 0,
                    "winningPosition": winner_dict[members] if members in winner_dict else 0
                }
                self.db_obj.upload_data(
                    new_member_obj, "Challenge_Member_Mapping")

    def check_unique_members(self, member_set: Set[str]):
        ''' Checks if the member already exists in the database and removes 
            from the set
        '''
        new_set = self.db_obj.check_member(member_set)
        self.member_set = new_set

    def upload_members(self, member_set: Set[str]):
        ''' Fetches from API and Uploads member to the database from the given member_set '''
        print(' Loading all unique members to the database ')
        member_progress = Bar(
            "Uploading Members", max=len(member_set))
        for member in member_set:
            try:
                processed_member = fetch_member_data(member)
                processed_member["user_entered"], processed_member["participation_skill"] = fetch_member_skills(
                    member)
            except Exception as e:
                print(e)
            else:
                self.db_obj.upload_data(processed_member, "Members")
            member_progress.next()
        member_progress.finish()
        print("Finished uploading all members to the DB")


# if __name__ == "__main__":
#     up = Uploader(
#         "/Users/mahirdhall/Desktop/WebScrapping/challengeData_2020-01-01_2020-02-02")
