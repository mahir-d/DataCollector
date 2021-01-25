import mysql.connector
import argparse

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

parser.add_argument('-pa', '--password', default='', type=str, metavar='password',
                    help="optional password, default set as an empty string '' ")


args = parser.parse_args()
print(args)
try:
    mydb = mysql.connector.connect(
        user=args.username,
        host=args.hostname,
        password='password'
    )
    print(mydb)
except mysql.connector.Error as err:
    print("ERROR")
    print(err)
