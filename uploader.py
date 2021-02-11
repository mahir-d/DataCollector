''' This file contains fuctions to upload processed data to database '''
import json
from os import listdir, getcwd, chdir
from os.path import isfile, join, isdir
from typing import Any, Dict, List, Set
from dbConnect import dbConnect
from fetch_functions import fetch_challenge_registrants, fetch_challenge_submissions, fetch_member_data
from progress.bar import Bar

class Uploader:
    ''' Ths class contains functions to uplod data to the database '''
    def __init__(self) -> None:
        self.db_config = {
            "username": "root",
            "hostname": "localhost",
            "password": "password",
            "port": "3306",
            "database": "dataCollector",
            "table_name": "Challenges"
        }
        self.db_obj = dbConnect(self.db_config)

    def uploadChallenges(self,directory):
        ''' Loads processed challenge from json file and upload it to DB while 
            fetching registrants and submissions from the API
        '''
        if not isdir(directory):
            raise NotADirectoryError(f'{directory} is not a valid directory')
        
        file_list = [file for file in listdir(directory)]
        
        if file_list:
            # Iterate over json challenges one file at a time
            # for each challenge one at a time, fetch its registrant members
            # fetch submission for the challenge
            # upload challenge to challenge table along with fill intermidiate table
            
            # Changes current working directory to the given directory
            chdir(directory)
            

            file_progress = Bar("ChargingBar", max=len(file_list))
            for file_name in file_list:
                try:
                    file_location = join(directory,file_name)
                    curr_json_file = open(file_location, "r")
                except OSError as exception:
                    print(exception)
                    print(f'File {file_name} could not be opened')
                else:
                    json_data = curr_json_file.read()
                    challenge_json = json.loads(json_data)
                    
                    challenge_progress = Bar("Bar", max=len(challenge_json))
                    for challenge in challenge_json:
                        self.load_challenge_members(challenge["challengeId"], challenge["winners"])
                        self.db_obj.upload_data(challenge, "Challenges")
                        challenge_progress.next()
                    challenge_progress.finish()
                    print(f'Finished loading challenges and all its members from {file_name}')
                file_progress.next()
            
            file_progress.finish()
                    
        else:
            print(f'No JSON files found in {directory}')
        
    def load_challenge_members(self,challenge_id: Dict[str,Any], challenge_winner: List[str]):
        ''' Fetches all registrants, submissions and winners, loads it to the mapping 
            database based on challenge_id and challenge_winner
        '''
        winners_list = challenge_winner.split(",")
        winner_dict: Dict[str,int] = {}
        for position, winner in enumerate(winners_list):
            winner_dict[winner] = position + 1

        submission_set: Set[str] = fetch_challenge_submissions(challenge_id)
        registrants_list: List[str] = fetch_challenge_registrants(challenge_id)

        for members in registrants_list:
            
            new_member_obj = {
                "challengeId": challenge_id,
                "memberHandle": members,
                "submission": 1 if members in submission_set else 0,
                "winningPosition": winner_dict[members] if members in winner_dict else 0
            }
            self.db_obj.upload_data(new_member_obj, "Challenge_Member_Mapping")


    def upload_members(self, member_list: List[str]):
        ''' Fetches from API and Uploads member to the database from the given member_list '''
        for member in member_list:
            try:
                processed_member = fetch_member_data(member)
            except Exception as e:
                print(e)
            else:
                self.db_obj.upload_data(processed_member, "Members")





if __name__ == "__main__":
    up = Uploader()

    # up.uploadChallenges(
    #     "/Users/mahirdhall/Desktop/WebScrapping/challengeData_2020-01-01_2020-02-02")
    
    mem = ["CreativeDroid",
    "ShindouHikaru",
    "talesforce",
    "Samkg143",
    "mahir_zzz"
    ]
    up.upload_members(mem)
