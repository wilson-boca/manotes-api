import os
from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from app import config as config_module
from app import api, database

config = config_module.get_config()

web_app = Flask(__name__)
web_app.config.from_object(config)
database.AppRepository.db = SQLAlchemy(web_app)
api.create_api(web_app)

def run():
    web_app.run(host='0.0.0.0', port=int(5324), debug=True)