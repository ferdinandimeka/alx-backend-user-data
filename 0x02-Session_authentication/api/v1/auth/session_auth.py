#!/usr/bin/env python3
'''Session Authentication views Module API
'''
from uuid import uuid4
from flask import request
from .auth import Auth
from models.user import User


class SessionAuth(Auth):
    ''' Session Authentication Class
    '''
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        ''' Create Session ID for users
        '''
        if user_id is None or type(user_id) != str:
            return None
        session_id = str(uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id
    
    def user_id_for_session_id(self, session_id: str = None) -> str:
        ''' Return User ID based on Session ID
        '''
        if session_id is None or type(session_id) != str:
            return None
        return SessionAuth.user_id_by_session_id.get(session_id)
    
    def current_user(self, request=None) -> User:
        ''' Return User instance based on cookie value
        '''
        session_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_cookie)
        return User.get(user_id)
    
    def destroy_session(self, request=None) -> bool:
        ''' Delete the user session / log out
        '''
        if request is None:
            return False
        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return False
        user_id = self.user_id_for_session_id(session_cookie)
        if user_id is None:
            return False
        del SessionAuth.user_id_by_session_id[session_cookie]
        return True
