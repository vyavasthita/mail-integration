<a name="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/vyavasthita/mail-integration">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Mail Integration</h3>

  <p align="center">
    Mail Integration Project!
    <br />
    <a href="https://github.com/vyavasthita/mail-integration/blob/master/README.md"><strong>Explore the docs »</strong></a>
    <br />
  </p>
</div>

<p align="right">(<a href="#readme-top">Back To Top</a>)</p>

# About the project
This project integrates with Gmail API and performs some rule based operations on emails.

Details:
* This project has been implemented using Python.
* This project lets user fetch gmails from a gmail account using official gmail api.
* These emails data and metadata are stored in Mysql database.
* User can apply filters and take action on these emails, say to move email to different label, by updating rules defined in a JSON file.

<p align="right">(<a href="#readme-top">Back To Top</a>)</p>

## Built With

Major softwares/libraries used in this project.

* [![Python][Python]][Python-url]
* [![Docker][Docker]][Docker-url]
* [![Docker Compose][Docker]][Docker-Compose-url]

<p align="right">(<a href="#readme-top">Back To Top</a>)</p>

## Testing
### Platform/Software
1. OS - Ubuntu 22.04
2. Docker Compose version v2.17.3
3. Docker version 23.0.6
4. Mysql 8.0.29
5. Python 3.10

### Scope
- Tested with english language search only.
- Tested without special characters search.
- Tested against Mysql InnoDB engine only.

### Assumptions
- Same email rule can be duplicated.

### Testing
- This app is tested on Ubuntu 22.04 LTS.
- Automated unit tests have been written using pytest.
- Automated Unit test coverage is 0%.

### Validations done
If invalid rule is provided in rule parser json file then application will exit.
01. Not connected to database

## :dart: Features
1. Mail Engine
    Connects with gmail api
    Fetches email content
    Parses email content
    Writes email content to database.

2. Rule Engine
    Reads selected rule from rules
    Generates Query based on rules
    Generates Actions based on rules
    Reads data from database based on query
    Updates Mail Server through RestAPIs.

If email script is run again, it will update the database.

- We can fetch emails by providing list of labels in config/<environment>/app_config.json

<p align="right">(<a href="#readme-top">Back To Top</a>)</p>

## :dart: Best Practices
- Use of context manager for db connection, gmail authentication
- Poetry for managing different environments
- Normalized DB Schema with Full text search index for pattern matching
- Python Logging - Console and File with proper log level
- Use of exception handling
- Doc string added for all modules and methods
- Type annotations are added for all methods.
- Docker with docker compose used.
- Use of environment variables.
- Unit tests with coverage report
- Detailed README file.
- Proper git commit messages. Every commit is done post completing a functionality.
- Pep8 naming convention for modules, classes, methods, functions and variables.
- Comments added wherever required.
- Use of decorators, dataclasses.
    Python Logging
- Use of Makefile to each in using the application.
- Manual steps are minimal while testing the app.
- Proper directory and file structure of source code.
- Import statements are in order.
    - Python core -> flask -> flask third party -> application modules

    Also related modules are imported in order.
- Different configurations for differnent environments like Dev, test, QA, Production.

<p align="right">(<a href="#readme-top">Back To Top</a>)</p>


## Technical Details

### Python Packages
Name: python-dotenv
Purpose: To read environment variables from .env files
Environment: All (development, qa, production etc.)

Name: google-api-python-client
Purpose: For gmail api
Environment: All (development, qa, production etc.)

Name: google-auth-httplib2
Purpose: For gmail api
Environment: All (development, qa, production etc.)

Name: google-auth-oauthlib
Purpose: For gmail api
Environment: All (development, qa, production etc.)

Name: BeautifulSoup4
Purpose: For decoding email body
Environment: All (development, qa, production etc.)

Name: lxml
Purpose: For decoding email body
Environment: All (development, qa, production etc.)

Name: mysql-connector-python
Purpose: To connect with mysql
Environment: All (development, qa, production etc.)

Name: dateutil
Purpose: To find date format of gmail datetime
Environment: All (development, qa, production etc.)

Name: black
Purpose: Python code formatting
Environment: development

Name: pytest
Purpose: Write automated tests
Environment: development

Name: pytest-cov
Purpose: Automated tests coverage
Environment: development

Name: requests-oauthlib
Purpose: OAuth2 for restapi using requests
Environment: All (development, qa, production etc.)

Name: requests
Purpose: Restapi using requests
Environment: All (development, qa, production etc.)

### DB Schema
CREATE TABLE IF NOT EXISTS label(  
    label_id varchar(25) NOT NULL,  
    name varchar(45) NOT NULL,  
    PRIMARY KEY (label_id)  
);

CREATE TABLE IF NOT EXISTS email(  
    message_id varchar(25) NOT NULL,
    is_read BOOLEAN,
    INDEX (is_read),
    PRIMARY KEY (message_id)
);

email_label(
    id int NOT NULL AUTO_INCREMENT,  
    label_id varchar(25) NOT NULL,
    message_id varchar(25) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (label_id) REFERENCES label(label_id),
    FOREIGN KEY (message_id) REFERENCES email(message_id)
);

email_sender(  
    message_id varchar(25) NOT NULL,
    sender varchar(255) NOT NULL,
    PRIMARY KEY (message_id),
    FOREIGN KEY (message_id) REFERENCES email(message_id),
    FULLTEXT (sender)
);

email_receiver(  
    message_id varchar(25) NOT NULL,
    receiver varchar(255) NOT NULL,
    PRIMARY KEY (message_id),
    FOREIGN KEY (message_id) REFERENCES email(message_id),
    FULLTEXT (receiver)
);

email_subject(  
    message_id varchar(25) NOT NULL,
    subject varchar(255) NOT NULL,
    PRIMARY KEY (message_id),
    FOREIGN KEY (message_id) REFERENCES email(message_id),
    FULLTEXT (subject)
);

email_content(  
    message_id varchar(25) NOT NULL,
    content MEDIUMTEXT NOT NULL,
    PRIMARY KEY (message_id),
    FOREIGN KEY (message_id) REFERENCES email(message_id),
    FULLTEXT (content)
);

email_date(  
    message_id varchar(25) NOT NULL,
    received date NOT NULL,
    PRIMARY KEY (message_id),
    INDEX (received),
    FOREIGN KEY (message_id) REFERENCES email(message_id)
);

### Source Code Folder Structure

```bash
|-- Dockerfile.dev
|-- Dockerfile.prod
|-- Dockerfile.qa
|-- Makefile
|-- README.md
|-- configuration
|   |-- development
|   |   |-- app_config.json
|   |   |-- email_rules.json
|   |   `-- logging.conf
|   |-- production
|   |   |-- app_config.json
|   |   |-- email_rules.json
|   |   `-- logging.conf
|   `-- qa
|       |-- app_config.json
|       |-- email_rules.json
|       `-- logging.conf
|-- credentials.json
|-- database
|   |-- development
|   |   |-- data
|   |   `-- sqls
|   |       |-- app_dev.sql
|   |       `-- test_dev.sql
|   |-- production
|   |   |-- data
|   |   `-- sqls
|   |       |-- app_production.sql
|   |       `-- test_production.sql
|   `-- qa
|       |-- data
|       `-- sqls
|           |-- app_qa.sql
|           `-- test_qa.sql
|-- docker
|-- docker-compose.dev.yaml
|-- docker-compose.prod.yaml
|-- docker-compose.qa.yaml
|-- entrypoint.sh
|-- images
|   `-- logo.png
|-- mail_helper.py
|-- poetry.lock
|-- poetry.toml
|-- pyproject.toml
|-- pytest.ini
|-- src
|   |-- __init__.py
|   |-- __pycache__
|   |-- api
|   |   |-- __init__.py
|   |   `-- api_request.py
|   |-- auth
|   |   |-- __init__.py
|   |   |-- auth.py
|   |   |-- connection.py
|   |   `-- gmail_auth.py
|   |-- config
|   |   |-- __init__.py
|   |   |-- app_config.py
|   |   `-- env_config.py
|   |-- data_layer
|   |   |-- __init__.py
|   |   |-- db_connection.py
|   |   |-- db_validation.py
|   |   |-- mail_dao.py
|   |   `-- sp_dao.py
|   |-- initialize.py
|   |-- mail_engine
|   |   |-- __init__.py
|   |   |-- mail_data.py
|   |   |-- mail_data_builder.py
|   |   |-- mail_engine.py
|   |   `-- mail_reader.py
|   |-- rule_engine
|   |   |-- __init__.py
|   |   |-- action_builder.py
|   |   |-- action_data.py
|   |   |-- query_builder.py
|   |   |-- rule_engine.py
|   |   |-- rule_parser.py
|   |   `-- rule_validation.py
|   `-- utils
|       |-- __init__.py
|       |-- __pycache__
|       |-- api_logger.py
|       |-- datetime_helper.py
|       |-- file_helper.py
|       |-- gen_credential_data.py
|       `-- json_reader.py
|-- tests
|   |-- __init__.py
|   |-- conftest.py
|   `-- unit
|       |-- __init__.py
|       |-- __pycache__
|       `-- test_api.py
`-- token.json
```

<p align="right">(<a href="#readme-top">Back To Top</a>)</p>

## Issues and Improvements
### Known issues
- If you switch build environments from developement to qa etc, then;-
  Stop the containers
  Clean the containers
  Start the containers

<!-- Getting Started -->
# 	:toolbox: Getting Started

This projects supports multiple build environments.
1. Development
2. QA
3. Production

Follow below steps to install the app.

<!-- Prerequisites -->
## :bangbang: Prerequisites

1. Docker must be installed
2. Docker compose must be installed
3. Git Version Control
4. GNU Make
5. Before using Google APIs, you need to turn them on in a Google Cloud project.

    You can turn on one or more APIs in a single Google Cloud project.

    Follow the given page and configure gmail api and download credential.json

    * Enable Gmail Api
    ```sh
    https://developers.google.com/gmail/api/quickstart/python
    ```

<!-- Installation -->
## :gear: Installation

Install my-project with npm

1. Clone the repo
   ```sh
   git clone https://github.com/vyavasthita/mail-integration.git
   ```

2. Go to root directory 'mail-integration'.
   ```sh
   cd mail-integration
   ```

3. Checkout master branch
   ```sh
   git checkout master
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

Choose one the below build environments for testing;-
Steps are similar for all the environments.

## :large_blue_circle: Development Build Environment

<!-- Env Variables -->
### :key: Environment Variables and Configuration

To run this project, you need to configure environment variables and configuration files

1. Set BUILD_ENV
   Set following environment variable.
   ```sh
   export BUILD_ENV=development
   ```
   Note: Default build environment is 'development' and hence if we do not set BUILD_ENV variable,
   we will be treated in development environment.

2. Go to directory 'configuration/development'
   ```sh
   cd configuration/development
   ```

3. Create .env files
    In this directory you will find two sample env files named '.env.app.sample' and '.env.test.sample'.

    From these two sample files we need to create two .env files

    a) .env.app
    This is used when running our application
    
    Rename '.env.app.sample' to '.env.app'.
    ```sh
    mv .env.app.sample .env.app
    ```

    Note: MYSQL_PASSWORD_APP's value is empty and its intentional. Keep 'MYSQL_PASSWORD_APP' blank only.

    b) .env.test
    This is used when running unit tests

    Rename '.env.test.sample' to '.env.test'.
    ```sh
    mv .env.test.sample .env.test
    ```
    Note: `MYSQL_PASSWORD_TEST` value is empty and its intentional. Keep `MYSQL_PASSWORD_TEST` blank only.
    
4. Update .env files
    - Update '.env.app' and '.env.test' files.
    
    Following variables in '.env.app' and '.env.test' should be available to you as part of enabling gmail app (as mentioned in prerequisite step).

    Update values of below environments from your credential.json file which you must have download from gmail.

    `CLIENT_ID_APP`=<str>
    `PROJECT_ID_APP`=<str>
    `AUTH_URI_APP`=<str>
    `TOKEN_URI_APP`=<str>
    `AUTH_PROVIDER_X509_CERT_URL_APP`=<str>
    `CLIENT_SECRET_APP`=<str>
    `REDIRECT_URIS_APP`=<str>
    `API_URL_APP`=<str>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

5. Paste the contents to  '.env.sample' in this development directory

    Rename '.env.sample' to '.env.app'

6. Update App Configuration (If required)
    In the current directory 'configuration/development' open 'app_config.json'.

    In the 'message' key, you can update 'max_email_read' and 'labels' as per your requirements.

    'max_email_read' determines how many max emails we want to fetch from gmail.
    'labels' determines which email lables we want to fetch from.

    'labels' is a list of strings.

    You probably want to keep it '[]' empty list only so that you can fetch emails from all the labels.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
   
7. Update email rules json file

    All the email rules, as per the requirements, are added in a json file

    In the current directory 'configuration/development' open 'email_rules.json'.

    You can update this file as per your testing scenario.

    Some information and validation points about this file; -

    - Key 'rule' is the name of the rule, you can use any name here.

    - Key 'predicate' can have only one of the two values 'all' or 'any'. (case sensitive)

    - Under key 'conditions', you can add N number of rules by adding more json.
      Each Field has an attribute 'code' associated with it. Following are the codes associated with fields.

      field: From -> Code: 1
      field: To -> Code: 2
      field: Subject -> Code: 3
      field: Message -> Code: 4
      field: Date received -> Code: 5

      Application is using these code (not field names) values to determine which condition to apply. And hence while adding/updating conditions, you need to make sure the value of code is given correctly as intended otherwise unexpected result may be encountered.

      It is perfectly fine to repeat a code twice (But make sure 'code' value is same in this case). Following condition is a valid one. This is applicable when predicate value is 'any', but for predicate 'all' duplicate condition may not yield any result.

        Below rule will fetch all those emails having word 'interviews' in subject plus those rules not having 'hello' in subject.

        {
            "field": "Subject",
            "code": 3,
            "predicate": {
                "type": "str",
                "code": 1,
                "name": "contains",
                "value": "interviews"
            }
        },
        {
            "field": "Subject",
            "code": 3,
            "predicate": {
                "type": "str",
                "code": 2,
                "name": "Does not contain",
                "value": "hello"
            }
        },


      Note: No validation is done to check if you entered a wrong code value say 50 or -1.

<p align="right">(<a href="#readme-top">Back To Top</a>)</p>

<!-- Run -->
## :running: Run Application

Now you are ready to start the application

1. Go back to project root directory 'mail-integration'.
   
   ```sh
   cd ..
   ```

2. Start containers

```bash
  make all
```

This will start 3 docker containers.
- Python App
- MySql DB
- Phpmyadmin

<p align="right">(<a href="#readme-top">Back To Top</a>)</p>
    
<!-- Running Tests -->
## :test_tube: Running Tests

To run tests, run the following command

```bash
  make test
```

<p align="right">(<a href="#readme-top">Back To Top</a>)</p>

<!-- Tests Coverage -->
## :test_tube: Unit Test Coverage

To run tests, run the following command

```bash
  make testcov
```
<p align="right">(<a href="#readme-top">Back To Top</a>)</p>

<!-- Stop containers -->
## :test_tube: Stop Containers

To stop all running containers, run the following command

```bash
  make stop
```

<p align="right">(<a href="#readme-top">Back To Top</a>)</p>

<!-- Clean containers -->
## :test_tube: Clean Containers

To clean all running containers, run the following command

```bash
  make clean
```

It will fun following commands
	docker network prune -f
	docker container prune -f
	docker image prune -f

Note: Be careful before you clean containers

<p align="right">(<a href="#readme-top">Back To Top</a>)</p>

<!-- Deployment -->
# :triangular_flag_on_post: Deployment

TBD

<p align="right">(<a href="#readme-top">Back To Top</a>)</p>

<!-- Usage -->
# :eyes: Usage

TBD

<p align="right">(<a href="#readme-top">Back To Top</a>)</p>


<!-- Roadmap -->
# :compass: Roadmap

I have used Full Text Search Indexes for searching the patterns.

It has some limitations;-
- [x] Full text indexes are created post insertions for performance reasons.
    Some words which are not searched.
        Ref: https://dev.mysql.com/doc/refman/8.1/en/fulltext-stopwords.html
    All searches/filtering are case-insensitive fashion.
    Full text search have minimum len of char..
        Ref: https://dev.mysql.com/doc/refman/8.0/en/fulltext-boolean.html

Some improvements are required, these are intentionly not done due to time constraints.
- [ ] Json rule validation is not done.
Searching/contains with special characters not tested.
7. More automated unit tests need to be written specially for db crud operations and also by using mocking.

8. Unit test coverage should improve.

10. Use some profiling tools to check performance

11. Use sphinx documentation


<p align="right">(<a href="#readme-top">Back To Top</a>)</p>

<!-- Contributing -->
## :wave: Contributing

<a href="https://github.com/vyavasthita/grhakarya/graphs/contributors">
  Contribution
</a>

<p align="right">(<a href="#readme-top">Back To Top</a>)</p>


<!-- Code of Conduct -->
### :scroll: Code of Conduct

TBD

<p align="right">(<a href="#readme-top">Back To Top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-url]: https://github.com/vyavasthita/grhakarya/graphs/contributors
[forks-url]: https://github.com/vyavasthita/mail-integration/network/members
[stars-url]: https://github.com/vyavasthita/mail-integration/stargazers
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/vyavasthita/mail-integration/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/diliplakshya/
[product-screenshot]: images/screenshot.png
[Python]: https://img.shields.io/badge/Python-000000?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[Docker]: https://img.shields.io/badge/Docker-4A4A55?style=for-the-badge&logo=docker&logoColor=FF3E00
[Docker-url]: https://www.docker.com/
[Docker-Compose-url]: https://docs.docker.com/compose/
