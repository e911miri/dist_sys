"""
API Server for onregistry web services
"""
import importlib
import json
import logging

from os import environ

from flask import Flask, jsonify, request, redirect, Response
from flask.ext.sqlalchemy import SQLAlchemy
from conf import rq_dashboard_settings, settings
from lib.auth import Authentication
from lib.controllers.rq_dashboard_controller import rq_dashboard_blueprint
from lib.simple_page import simple_page
from lib.helpers.queue_helper import heartbeat

from mongoengine import register_connection
from mongoengine.errors import NotUniqueError
from redis import StrictRedis
from rq import Queue
import rq_dashboard

APP = Flask(__name__)

AUTH = Authentication()
REDIS = StrictRedis(host='redis')
Q = Queue(connection=REDIS)

if 'TEST' not in environ or not environ['TEST']:
    register_connection('default',
                        'onregistry',
                        environ['MONGO_PORT_27017_TCP_ADDR'],
                        27017)
    REDIS = StrictRedis(host='redis')

import lib.routes.asset
import lib.routes.user
APP.config.from_object(rq_dashboard_settings)
APP.config.from_object(settings.DevelopmentConfig)
APP.register_blueprint(rq_dashboard_blueprint,
                        static_folder='static',
                        url_prefix='/rq')
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
POSTGRES = SQLAlchemy(APP)

from lib.models.sql import Asset

@APP.route('/')
@AUTH.requires_auth
def api_live():
    """ root endpoint; serves to notify that the application is live """
    return Response(json.dumps({'message' : 'Api is live.'}), 200)

@APP.route('/urls')
def urls():
    APP.logger.info(APP.config)
    APP.logger.info(rq_dashboard_blueprint.static_url_path)
    APP.logger.info(environ)
    return Response(json.dumps({'message' : str(APP.url_map)}), 200)

@APP.route('/jumpstart')
def jumpstart():
    result = Q.enqueue(heartbeat)
    return Response(json.dumps({'message' : "It's alive!"}), 200)
