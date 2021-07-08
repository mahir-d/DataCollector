
<h1 align="center">Welcome to DataCollector 👋</h1>

### 🏠 [Homepage](https://github.com/mahir-d/DataCollector#README.md)

## Introduciton
Provides the following functionalities:
 * Fetches publically available data on challenges and member information from a crowd-sourced development platform
 * Uploads to Sql database
 * Converts the database to Excel Sheet


## Install
Execute the following command to load all the project dependencies
```sh
$ pip install -r requirements.txt
```

### Set up
 - Create a `.env` file in the root directory of your project.
 - Add environment-specific variables on new lines in the form of 
   `NAME=VALUE`.
- Requried varibales and sample values based on MySql configurations
- `authKey` is the authorization bearer token that can be found from the network inspect in the browser's developer mode

*Sample .env file with all required variables*
```dosini
dbUsername=root
dbHostname=localhost
dbPassword=password
dbPort=3306
databaseName=dataCollector_v2
authKey=""
```

## Run

 - [x] **Make sure your MySQL server is up and running before executing the program**

To start fetching and downloading challenges and memeber information execute automation.py file with the following positional arguments space seperated:

``` sh
positional arguments:
  Start_year  Please enter start year to fetch challenges and members from
  End_year    Please enter end year to fetch challenges and members till
              inclusive
  Status      Please choose the status of the challenges to be fetched.
              Default set as Completed
  path        Path to the directory to store data

optional arguments:
  -h, --help  show this help message and exit
```

For example, Execute the following command to start downloading challenges and memebers and storing them in database with configurations as mentioned in the  [.env file]
``` sh
$ python automation.py 2020 2021 Completed
```

## Convert database Table to excel
Once all the Challenges and member information is downloaded in the MySQL database, it can be easily converted to an Excel sheet by executing the command using the following positional argument space seperated:

``` sh
positional arguments:
  Table_name  Please select table name to be converted to excel sheet

optional arguments:
  -h, --help  show this help message and exit
```

For example, Execute the following command to convert table from the database with configurations as mentioned in the  [.env file]
```sh
$ python dbConnect.py Challenges
```

**The converted Excel sheets will be stored in the root directory of the DataCollector project**

## Author
👤 **Mahir Dhall**
