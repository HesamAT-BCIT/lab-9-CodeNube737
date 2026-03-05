import os
from flask import request, jsonify
from functools import wraps
import firebase_admin.auth

# Decorator to require API key for sensor data POST

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-KEY')
        expected_key = os.environ.get('SENSOR_API_KEY')
        if not api_key or api_key != expected_key:
            return jsonify({'error': 'Invalid or missing API key'}), 401
        return f(*args, **kwargs)
    return decorated_function

# Decorator to require JWT for protected routes

def require_jwt(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Missing or invalid Authorization header'}), 401
        token = auth_header.split(' ')[1]
        try:
            decoded_token = firebase_admin.auth.verify_id_token(token)
            uid = decoded_token['uid']
        except Exception:
            return jsonify({'error': 'Invalid or expired token'}), 401
        return f(uid, *args, **kwargs)
    return decorated_function
