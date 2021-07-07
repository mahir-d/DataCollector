<h1 align="center">Welcome to DataCollector 👋</h1>

### 🏠 [Homepage](https://github.com/mahir-d/DataCollector#README.md)

## Introduciton
Provides the following functionalities:
 * Fetches publically available data on challenges and member information from a crowd-sourced development platform
 * Uploads to Sql database
 * Converts the database to Excel Sheet


``` 

## Install
Execute the following command to load all the project dependencies
```sh
$ pip install -r requirements.txt
```

### Set up
Create a `.env` file in the root directory of your project. Add
environment-specific variables on new lines in the form of `NAME=VALUE`.
Requried varibales and sample values based on MySql configurations

```dosini
dbUsername=root
dbHostname=localhost
dbPassword=password
dbPort=3306
databaseName=dataCollector_v2
authKey=""
```


## Run

Execute the following command to start the sever at the PORT number mentioned
in the [.env file](#set-up)
``` sh
npm start
```

## Run tests
Run the following command to seed and run the Test database in testing enviroment
```sh
npm run test
```

## API documentation
To look up the API documentation, please start the local sever by executing the [run command](#run)
and then redirect to the follwing url by adding the port number mentioned in the [.env file](#set-up)
``` url
http://localhost:{port}/api-docs
```

## Author

👤 **Mahir Dhall**

* Github: [@mahir-d](https://github.com/mahir-d)

## 🤝 Contributing

Contributions, issues and feature requests are welcome!<br />Feel free to check [issues page](https://github.com/mahir-d/smart-construction-dashboard/issues). You can also take a look at the [contributing guide](https://github.com/mahir-d/smart-construction-dashboard/blob/master/CONTRIBUTING.md).

## 📝 License

Copyright © 2021 [Mahir Dhall](https://github.com/mahir-d).<br />
This project is [ISC](https://github.com/mahir-d/smart-construction-dashboard/blob/master/LICENSE) licensed.

