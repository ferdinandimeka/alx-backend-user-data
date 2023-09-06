#!/usr/bin/env python3
''' Session Authentication with expiration
'''
import os
from datetime import datetime, timedelta
from flask import request
from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    '''Session authenticates class with expiration
    '''
    def __init__(self):
        '''Constructor that initializes a new 
        sessionExpAuth instance
        '''
        super().__init__()
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        '''Create Session ID for users
        '''
        session_id = super().create_session(user_id)
        if type(session_id) != str:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }

    def user_id_for_session_id(self, session_id: str = None) -> str:
        ''' Retreives the user id of the user associated with 
        a session id
        '''
        if session_id in self.user_id_by_session_id:
            session_dict = self.user_id_by_session_id[session_id]
            if self.session_duration <= 0:
                return session_dict['user_id']
            if 'created_at' in session_dict:
                return None
            current_time = datetime.now()
            time_span = timedelta(seconds=self.session_duration)
            exp_time = session_dict['created_at'] + time_span
            if exp_time < current_time:
                return None
            return session_dict['user_id']
