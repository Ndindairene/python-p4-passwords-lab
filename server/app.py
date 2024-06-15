#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource

from config import app, db, api
from models import User

class ClearSession(Resource):

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204

class Signup(Resource):
    
    def post(self):
        json = request.get_json()
        user = User(
            username=json['username']
        )
        user.password_hash = json['password']
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 201

class CheckSession(Resource):
    
    def get(self):
        user_id = session.get('user_id')
        
        if user_id:
            # Fetch the user from the database
            user = User.query.get(user_id)
            if user:
                return user.to_dict(), 200
        
        # No authenticated user found
        return {}, 204


class Login(Resource):
    
    def post(self):
        json_data = request.get_json()
        username = json_data.get('username')
        password = json_data.get('password')
        
        if not username or not password:
            return {'message': 'Username and password are required'}, 400
        
        # Retrieve the user from the database
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            # Password is correct, log the user in
            session['user_id'] = user.id
            return user.to_dict(), 200  # Assuming to_dict() method returns a dictionary
        
        # Invalid credentials
        return {'message': 'Invalid username or password'}, 401
class Logout(Resource):
    
    def delete(self):
        session.pop('user_id', None)
        return {}, 204

api.add_resource(ClearSession, '/clear', endpoint='clear')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')

if __name__ == '__main__':
    app.run(port=5555, debug=True)

