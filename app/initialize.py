# -*- coding: utf-8 -*-
import datetime
from flask import Flask, g, request
from flask_sqlalchemy import SQLAlchemy
# from flask_cors import CORS
from app import database, config as config_module
from app.async_tasks import establish


config = config_module.get_config()
web_app = Flask(__name__)
web_app.config.from_object(config)

establish.make_worker(web_app)
worker = establish.worker
establish.register_tasks(worker)


# CORS(
#     web_app, origins="*",
#     allow_headers=[
#         "Content-Type",
#         "Authorization",
#         "Access-Control-Allow-Credentials"
#     ],
#     supports_credentials=True
# )

database.AppRepository.db = SQLAlchemy(web_app)


@web_app.before_request
def before_request():
    from app.security import authentication
    token = request.cookies.get('userToken')
    authentication.AuthService.authenticate_with_token(token)


@web_app.after_request
def add_token_header(response):
    user = g.get("user")
    if user is not None:
        token = g.current_token
        expire_date = datetime.datetime.now()
        expire_date = expire_date + datetime.timedelta(days=90)
        response.set_cookie('userToken', token, expires=expire_date)

    return response


def create_api():
    from app import api
    api.create_api(web_app)


def run():
    create_api()
    web_app.run(host='0.0.0.0', port=int(config.PORT), debug=True)
