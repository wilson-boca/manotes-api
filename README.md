# manotes-api

A Python restful-api sample.

### Test coverage
[![Coverage Status](https://coveralls.io/repos/github/antunesleo/manotes-api/badge.svg?branch=master)](https://coveralls.io/github/antunesleo/manotes-api?branch=master)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

* Linux
* Python 3+
* Pip3
* Virtualenvwrapper (optional but recommended)
* PostgreSQL 10+ 

### Installing

Installing requirements
```
$ sudo apt-get install redis-server
$ git clone git@github.com:antunesleo/manotes-api.git
$ mkvirtualenv manotes-api (Optional)
$ workon manotes-api (Optional)
$ pip install -r requirements.txt
$ pip install -r requirements_dev.txt
```
Dealing with environments variables

```
$ cd
$ vim .bashrc

Add this in the end of file and reopen the terminal
alias load-env='export $(cat .env | xargs)'
alias load-env-test='export $(cat .env.test | xargs)'

$ load-env
```

Setting up database
```
$ sudo apt-get install postgres
$ sudo su postgres
$ psql
$ CREATE ROLE manotes SUPERUSER LOGIN PASSWORD 'manotes'
$ CREATE DATABASE manotes
$ ALTER DATABASE manotes OWNER TO manotes;
$ \q
$ exit

Create a .env file based on .env.sample, with your custom configuration (if necessary) and then:
$ load-env
$ python manage.py db upgrade

```

## Running the tests
```
load-env-test
python -m testtools.run
```

## Running API
```
load-env
python run.py
```

## Features
| Features        | Description   |
| -------------   |:-------------:| 
| Login | [POST] in the endpoint 'api/login' unauthenticated users can login |
| Create Account  | [POST] in the endpoint 'api/account' users can create account passing email, username and password| 
| Update Account  | [PUT] in the endpoint 'api/account' authenticated users can update account infos passing email and/or username| 
| Update Avatar   | [PUT] in the endpoint 'api/avatar' authenticated users can update avatar passing a file binary keyed avatar
| Create Note     | [POST] in the endpoint 'api/notes' authenticated user can create a note passing name, content and color |
| Update Note     | [PUT] in the endpoint 'api/notes' authenticated user can update a note passing name, content and color |
| Get Note        | [GET] in the endpoint 'api/notes/<note_id>' authenticated user can list all notes or get a specific note if note_id is passed |
| Delete Note     | [DELETE] in the endpoint 'api/notes/<note_id>' authenticated user can delete a note |


## Built With

* [Alembic](http://alembic.zzzcomputing.com/en/latest/) - lightweight database migration tool for usage with the SQLAlchemy Database Toolkit
* [boto3](https://pypi.org/project/boto3/) - AWS SDK for Python, which allows Python developers to write software that makes use of services like S3.
* [celery](https://pypi.org/project/celery/) - Distributed task queue
* [Flask](http://flask.pocoo.org/) - The web framework used
* [flask-CORS](https://flask-cors.readthedocs.io/en/latest/) - A Flask extension for handling Cross Origin Resource Sharing (CORS), making cross-origin AJAX possible.
* [Flask Migrate](https://flask-migrate.readthedocs.io/en/latest/) - an extension that handles SQLAlchemy database migrations for Flask applications using Alembic.
* [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/) - an extension for Flask that adds support for quickly building REST APIs
* [gunicorn](https://pypi.org/search/?q=gunicorn) - a Python WSGI HTTP Server for UNIX
* [mock](https://pypi.org/project/mock/) - mock is a library for testing in Python. It allows you to replace parts of your system under test with mock objects and make assertions about how they have been used.
* [passlib](https://pypi.org/project/passlib/) - comprehensive password hashing framework
* [pip](https://pypi.org/project/pip/) - Dependency Management
* [Psycopg](http://initd.org/psycopg/) - PostgreSQL adapter for the Python programming language
* [SQLAlchemy](https://www.sqlalchemy.org/) - Python SQL toolkit and Object Relational Mapper
* [SQLAlchemy-Utils](https://pypi.org/project/SQLAlchemy-Utils/) - Various utility functions for SQLAlchemy.
* [testtools](http://testtools.readthedocs.io/en/latest/for-test-authors.html) - testtools is a set of extensions to Python’s standard unittest module.

## Authors

* **Leonardo Antunes** - *Initial work* - [antunesleo](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments
pass
