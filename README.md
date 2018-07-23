# manotes-api

A Python restful-api sample.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

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
python -m testtools.run
```
## Features
| Features        | Description   |
| -------------   |:-------------:| 
| Create Account  | [POST] in the endpoint 'api/account' unknow users can create account passing email, username and password| 
| Update Account  | [PUT] in the endpoint 'api/account' authenticated users can update account infos passing email and/or username| 
| Create Note     | [POST] in the endpoint 'api/notes' authenticated user can create a note passing name, content and color |
| Update Note     | [PUT] in the endpoint 'api/notes' authenticated user can update a note passing name, content and color |
| Get Note        | [GET] in the endpoint 'api/notes/<note_id>' authenticated user can list all notes or get a specific note if note_id is passed |
| Delete Note     | [DELETE] in the endpoint 'api/notes/<note_id>' authenticated user can delete a note |

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Flask](http://flask.pocoo.org/) - The web framework used
* [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/) - an extension for Flask that adds support for quickly building REST APIs
* [Psycopg](http://initd.org/psycopg/) - PostgreSQL adapter for the Python programming language
* [SQLAlchemy](https://www.sqlalchemy.org/) - Python SQL toolkit and Object Relational Mapper
* [Alembic](http://alembic.zzzcomputing.com/en/latest/) - lightweight database migration tool for usage with the SQLAlchemy Database Toolkit
* [Flask Migrate](https://flask-migrate.readthedocs.io/en/latest/) - an extension that handles SQLAlchemy database migrations for Flask applications using Alembic.
* [flask-CORS](https://flask-cors.readthedocs.io/en/latest/) - A Flask extension for handling Cross Origin Resource Sharing (CORS), making cross-origin AJAX possible.
* [pip](https://pypi.org/project/pip/) - Dependency Management
* [mock](https://pypi.org/project/mock/) - mock is a library for testing in Python. It allows you to replace parts of your system under test with mock objects and make assertions about how they have been used.
* [testtools](http://testtools.readthedocs.io/en/latest/for-test-authors.html) - testtools is a set of extensions to Python’s standard unittest module.

## Contributing

Please read [CONTRIBUTING.md](https://example.com) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Leonardo Antunes** - *Initial work* - [antunesleo](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
