from __future__ import annotations

from functools import wraps
from typing import Optional, Tuple, Union
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Response
from flask.typing import ResponseReturnValue
import firebase_admin
from firebase_admin import credentials, firestore, auth
from firebase_admin.firestore import DocumentReference
import os
import re
import requests
import time

from flask import Flask
from config import Config

# Import blueprints
from blueprints.auth import auth_bp
from blueprints.profile import profile_bp
from blueprints.dashboard import dashboard_bp
from blueprints.api import api_bp

app = Flask(__name__)
app.config.from_object(Config)

# Register blueprints
app.register_blueprint(dashboard_bp)  # Handles root route /
app.register_blueprint(auth_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(api_bp)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
