# -*- coding: utf-8 -*-
import datetime
from flask import Flask, g, request
from flask_sqlalchemy import SQLAlchemy
from app import config as config_module, authentication
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


@web_app.before_request
def before_request():
    token = request.cookies.get('userToken')
    authentication.AuthService.authenticate_token(token)


@web_app.after_request
def add_token_header(response):
    user = g.get("user")
    if user is not None:
        token = g.current_token

        expire_date = datetime.datetime.now()
        expire_date = expire_date + datetime.timedelta(days=90)
        response.set_cookie('userToken', token, expires=expire_date)

    return response


def run():
    web_app.run(host='127.0.0.1', port=int(5324), debug=True, threaded=True)
