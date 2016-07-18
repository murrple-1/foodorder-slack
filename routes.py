"""
Routes and views for the bottle application.
"""

from bottle import get, route, hook, response
import sqlite3
import os

@hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = os.environ.get("ALLOW_ORIGIN") or '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With'

@route('/<:re:.*>', method='OPTIONS')
def options():
    return ''

@get("/")
def index_get():
    return "Food Order Slack-Bot"
