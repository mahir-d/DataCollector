''' This file contains methods to connect to Mysql database and convert db to excel sheet '''
from typing import List, Set
import mysql.connector
from mysql.connector import errorcode
import argparse
import tableColumnName
from progress.bar import Bar
import xlsxwriter
from dotenv import load_dotenv
from os import environ

class dbConnect:
    def __init__(self, args) -> None:
        self.db_username = args['username']
        self.db_hostname = args['hostname']
        self.db_password = args['password']
        self.db_port = args['port']
        self.db_name = args['database']
        self.db_connection = ''
        self.table_name = args['table_name']

        # Connects to the Mysql server
        self.connect_db_server()
        # Connects to the given database
        self.check_database(self.db_name)
        # Checks if the table exists otherwise creates it
        self.check_table("Challenges")
        self.check_table("Challenge_Member_Mapping")
        self.check_table("Members")

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
        db_obj.execute(f'CREATE DATABASE IF NOT EXISTS {database_name}')

        db_obj.execute(f'USE {self.db_name}')
        print('Database created')

    def check_table(self, table_name: str):
        ''' Checks if table exists otherwise creates it in database '''
        db_obj = self.db_connection.cursor()

        try:
            table_col_obj = tableColumnName.TableColumnName()
            db_obj.execute(
                f'CREATE TABLE IF NOT EXISTS {table_name} ({table_col_obj.__getattribute__(table_name)["col_name_create"]})')
            print('table created')
        except mysql.connector.Error as err:
            print(f'table could not be created cause of Error: {err}')

    def check_member(self, member_set: Set[str]) -> Set[str]:
        ''' Checks if the member already exists in the database '''
        db_obj = self.db_connection.cursor()

        try:
            db_obj.execute(
                f'SELECT memberHandle FROM Members')

            existing_member_set: List[str] = list(
                [memberHandle[0] for memberHandle in db_obj])
            member_check = Bar(
                "Check Members Exists", max=len(existing_member_set))
            for memberHandle in existing_member_set:

                if memberHandle in member_set:
                    member_set.remove(memberHandle)
                member_check.next()
            member_check.finish()
            return member_set

        except mysql.connector.Error as err:
            print(f'Error: {err}')

    def upload_data(self, challenge_data, table_name) -> bool:
        ''' Uploads the given data to the appropriate Database table '''
        db_obj = self.db_connection.cursor()
        table_col_obj = tableColumnName.TableColumnName()
        val_to_insert = [val for val in challenge_data.values()]
        s_list = ["%s" for i in range(len(val_to_insert))]
        s_str = ",".join(s_list)
        try:
            sql_query = f'INSERT INTO {table_name} ({table_col_obj.__getattribute__(table_name)["col_name_insert"]}) VALUES ({s_str})'
            db_obj.execute(sql_query, val_to_insert)
            self.db_connection.commit()
            return db_obj.lastrowid
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            elif err.errno == 1406:
                print(err)
            else:
                print(err)
            return -1

    def excel_uploader(self, table_name: str) -> None:
        ''' Uploads sql data to excel sheet '''
        db_obj = self.db_connection.cursor()
        table_col_obj = tableColumnName.TableColumnName()
        col_names: List[str] = table_col_obj.__getattribute__(table_name)[
            "sql_col_name_insert"].split(",")

        workbook = xlsxwriter.Workbook(f'{table_name}.xlsx')
        worksheet = workbook.add_worksheet()
        format3 = workbook.add_format({'num_format': 'mm/dd/yy'})

        # Add column names
        row: int = 0
        col: int = 0
        for col_name in col_names:
            worksheet.write(row, col, col_name)
            col += 1
        row += 1
        col = 0
        try:
            sql_query = f'SELECT * FROM {table_name};'
            db_obj.execute(sql_query)

            if table_name == "Challenges":
                for data in db_obj:
                    for col_data in data:
                        if col >= 11 and col <= 16:
                            worksheet.write(row, col, col_data, format3)
                        else:
                            worksheet.write(row, col, col_data)
                        col += 1
                    row += 1
                    col = 0
            else:
                for data in db_obj:
                    for col_data in data:
                        worksheet.write(row, col, col_data)
                        col += 1
                    row += 1
                    col = 0

        except mysql.connector.Error as err:
            print(err)

        workbook.close()


if __name__ == "__main__":


    parser = argparse.ArgumentParser(prog='dbConnector',
                                     usage='%(prog)s [options] path',
                                     description='connects the Mysql databse to upload the data',
                                     epilog="Made by Mahir Dhall"
                                     )

    parser.add_argument('Table_name', metavar="Table_name" ,choices=['Challenge_Member_Mapping', 'Challenges', 'Members'], default='Challenges', help="Please select table name to be converted to excel sheet")


    args = parser.parse_args()

    load_dotenv()
    db_Config = {
        "username": environ.get("dbUsername"),
            "hostname": environ.get("dbHostname"),
            "password": environ.get("dbPassword"),
            "port": environ.get("dbPort"),
            "database": environ.get("databaseName"),
            "table_name": "Challenges"
    }

    db = dbConnect(db_Config)
    db.excel_uploader(args.Table_name)
    

    # parser.add_argument('-ho', '--hostname', type=str, metavar='hostname',
    #                     default='localhost',
    #                     help="Optional hostname, default set as localhost")

    # parser.add_argument('-po', '--port', type=str, metavar="port",
    #                     default='3306', help="optional port number, default set as 3306")

    # parser.add_argument('-u', '--username', type=str, default="root",
    #                     help="optional username, default set as root")

    # parser.add_argument('-pa', '--password', default='password', type=str, metavar='password',
    #                     help="optional password, default set as an empty string '' ")

    # parser.add_argument('-db', '--database', metavar='database_name', type=str,
    #                     help='optional Database name, default set as dataCollector',
    #                     default='dataCollector')

    # parser.add_argument('-t', '--table_name', default='Challenges',
    #                     help='optional Table name, default set as Challenges')

    
