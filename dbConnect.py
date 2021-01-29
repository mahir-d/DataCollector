import mysql.connector
from mysql.connector import errorcode
import argparse


class dbConnect:
    def __init__(self, args) -> None:
        self.db_username = args.username
        self.db_hostname = args.hostname
        self.db_password = args.password
        self.db_port = args.port
        self.db_name = args.database
        self.db_connection = ''

        self.connect_db_server()
        self.check_database(self.db_name)

        self.check_table('Challenges')
        self.db_connection.close()

    def connect_db_server(self):
        ''' Makes the connection with the MySql database usin the provided config '''
        try:
            print("Making connection to the Mysql server..")
            mydb = mysql.connector.connect(
                user=self.db_username,
                host=self.db_hostname,
                password=self.db_password
            )
            self.db_connection = mydb
            print("Mysql server connected Successfully..")

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def check_database(self, database_name: str):
        ''' Checks if database exists otherwise creates it '''
        db_obj = self.db_connection.cursor()
        print(db_obj.execute("SHOW DATABASES"))

        if database_name not in db_obj:
            print("does not exists")
            db_obj.execute(
                f'CREATE DATABASE IF NOT EXISTS {database_name}')

            db_obj.execute(f'USE {self.db_name}')
            print('Database created')

        else:
            print("Database exists")

    def check_table(self, table_name: str):
        ''' Checks if table exists otherwise creates it in database '''
        db_obj = self.db_connection.cursor()

        try:
            db_obj.execute(
                f'CREATE TABLE IF NOT EXISTS {table_name} (challengeId VARCHAR(50) PRIMARY KEY, challengeName VARCHAR(512), legacyId VARCHAR(10), status VARCHAR(10), challengeTrack VARCHAR(20), challengeType VARCHAR(20), forumId VARCHAR(20), directProjectId VARCHAR(20) , legacyProjectId VARCHAR(20), challengeDescription MEDIUMTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL, createdOn DATETIME, registrationStartDate DATETIME, registrationEndDate DATETIME, submissionStartDate DATETIME, submissionEndDate DATETIME, Tags VARCHAR(512), numOfSubmissions INT(4), numOfRegistrants INT(4), winners INT(4), totalPrizeCost INT(10))')
            print('table created')
        except mysql.connector.Error as err:
            print(f'table could not be created cause of {err}')

        # my_cursor.execute("SHOW TABLES")

        # for x in my_cursor:
        #     print(x)


def main(args):
    db = dbConnect(args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='dbConnector',
                                     usage='%(prog)s [options] path',
                                     description='connects the Mysql databse to upload the data',
                                     epilog="Made by Mahir Dhall"
                                     )

    parser.add_argument('-ho', '--hostname', type=str, metavar='hostname',
                        default='localhost',
                        help="Optional hostname, default set as localhost")

    parser.add_argument('-po', '--port', type=str, metavar="port",
                        default='3306', help="optional port number, default set as 3306")

    parser.add_argument('-u', '--username', type=str, default="root",
                        help="optional username, default set as root")

    parser.add_argument('-pa', '--password', default='password', type=str, metavar='password',
                        help="optional password, default set as an empty string '' ")

    parser.add_argument('-db', '--database', metavar='database_name', type=str,
                        help='optional Database name, default set as dataCollector',
                        default='dataCollector')

    args = parser.parse_args()

    main(args)
