import os
from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from app import config as config_module
from app import api, database
from flask_cors import CORS

config = config_module.get_config()

web_app = Flask(__name__)
web_app.config.from_object(config)
CORS(
    web_app, origins="*",
    allow_headers=[
        "Content-Type",
        "Authorization",
        "Access-Control-Allow-Credentials"
    ],
    supports_credentials=True
)
database.AppRepository.db = SQLAlchemy(web_app)
api.create_api(web_app)


def run():
    web_app.run(host='0.0.0.0', port=int(5324), debug=True, threaded=True)
