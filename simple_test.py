#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
CORS(app)

# PostgreSQL database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'postgresql://avnadmin:AVNS_QzflMrR3BXGAgudXgwL@'
    'pg-7fabea4-nikshithkyathrigi2005-3753.g.aivencloud.com:14586/defaultdb'
    '?sslmode=require'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
db.init_app(app)

class SimpleUser(db.Model):
    __tablename__ = 'simple_users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'Simple Flask server is working!', 'status': 'success'})

@app.route('/db_test', methods=['GET'])
def db_test():
    try:
        # Try to query the database
        users = SimpleUser.query.all()
        return jsonify({
            'message': 'Database connection successful',
            'user_count': len(users),
            'status': 'success'
        })
    except Exception as e:
        return jsonify({
            'message': f'Database error: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/create_user', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        username = data.get('username', 'test_user')
        
        user = SimpleUser(username=username)
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'User created successfully',
            'username': username,
            'status': 'success'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'message': f'Error creating user: {str(e)}',
            'status': 'error'
        }), 500

if __name__ == '__main__':
    print("Starting simple Flask test server...")
    try:
        with app.app_context():
            print("Creating database tables...")
            db.create_all()
            print("✓ Database tables created successfully")
    except Exception as e:
        print(f"✗ Database initialization error: {e}")
    
    print("Starting Flask server on port 5004...")
    app.run(host='0.0.0.0', port=5004, debug=True, threaded=True)

