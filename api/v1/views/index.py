#!/usr/bin/python3
"""
Module for methods used by app_view blueprint
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """that returns a JSON: "status": 'OK'"""
    return jsonify({'status': 'OK'})
