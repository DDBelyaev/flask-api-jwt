from . import app, db, bcrypt, mail, BASEDIR
from .models import User
from flask import Blueprint, jsonify, request, current_app, send_file, send_from_directory
from flask_mail import Message

from functools import wraps
from datetime import datetime, timedelta
import os

import jwt

@app.route('/api/login/', methods=('POST',))
def login():
    data = request.get_json()
    print(data)
    user = User.authenticate(**data)

    print(current_app.config['SECRET_KEY'])

    if not user:
        return jsonify({ 'message': 'Invalid credentials', 'authenticated': False }), 401

    token = jwt.encode({
        'sub': user.email,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=30)},
        current_app.config['SECRET_KEY'])
    return jsonify({ 'token': token.decode('UTF-8') })

def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()
        print(request, request.headers, auth_headers, sep='\n')
        invalid_msg = {
            'message': 'Invalid token. Registeration and / or authentication required',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token. Reauthentication required.',
            'authenticated': False
        }

        if len(auth_headers) != 2:
            print(invalid_msg)
            return jsonify(invalid_msg), 401

        try:
            token = auth_headers[1]
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            user = User.query.filter_by(email=data['sub']).first()
            if not user:
                raise RuntimeError('User not found')
            return f(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401 # 401 is Unauthorized HTTP status code
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return jsonify(invalid_msg), 401

    return _verify

@app.route('/api/ping', methods=['GET', 'POST'])
@token_required
def ping():
  data = request.get_json()
  print(data)

  msg = Message(f'{data}', recipients = ['test@test.com'])
  with app.open_resource(os.path.join('files', 'test.txt')) as file:
      msg.attach(os.path.join('files', 'text.txt'), 'text/plain', file.read())
  mail.send(msg)
  return send_file(os.path.join(BASEDIR, 'files', 'test.txt'), mimetype="text/plain", as_attachment=True)

