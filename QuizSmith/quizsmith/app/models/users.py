#
#   Copyright 2014 UW Board of Regents
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

from sqlalchemy import Integer,String,Unicode,Boolean,TIMESTAMP,ForeignKey,Table
from sqlalchemy.orm import relation
from formalchemy import Column, fields
from fa.jquery import renderers
from hashlib import sha1
from quizsmith.app.models import Base,DBSession,TriviaModel
import os,transaction,datetime


UsersGroups = Table('users_groups', Base.metadata,
    Column('users_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('groups_id', Integer, ForeignKey('groups.id'), primary_key=True),
)

class Users(Base,TriviaModel):
    __tablename__ = 'users'
    __label__ = 'User' # fa scaffold
    __plural__ = 'Users' # fa scaffold
    
    id = Column(Integer, primary_key=True, label='User ID')
    is_local = Column(Boolean, label='Local User')
    email = Column(Unicode(25), unique=True, label='Email')
    password = Column(Unicode(255), label='Password', renderer=fields.HiddenFieldRenderer, readonly=True)
    fullname = Column(Unicode(55), label='Full Name')
    alias = Column(Unicode(25), label='Alias')
    groups = relation('Groups', secondary='users_groups')
    current_test = Column(Integer, label='Active Test')
    current_question = Column(Integer, label='Active Question')
    needs_accessibility = Column(Boolean, label='Needs Accessibility')
    last_active = Column(TIMESTAMP, default=datetime.datetime.now())

    def __init__(self, **kwargs):
        self.email = kwargs.get('email','')
        self._set_password(kwargs.get('password',None))
        self.fullname = kwargs.get('fullname',None)
        self.alias = kwargs.get('alias',None)
        self.is_local = kwargs.get('is_local',True)
        self.groups = kwargs.get('groups',[])
        self.current_test = 0
        self.current_question = 0
        self.needs_accessibility = kwargs.get('needs_accessibility',False)
    
    @classmethod
    def registerLocalUser(cls, email='', password='', groups=None):
        from quizsmith.app.models import Groups
        if groups == None:
            groups = [Groups.by(3).first()]
        user = Users(email=email, password=password, groups=groups)
        DBSession.add(user)
        transaction.commit()
        
    @classmethod
    def registerNonLocalUser(cls, email='', fullname='', groups=None):
        from quizsmith.app.models import Groups
        if not groups:
            groups = [Groups.by(3).first()]
        user = Users(email=email, fullname=fullname, is_local=False, groups=groups)
        DBSession.add(user)
        transaction.commit()

    @classmethod
    def login_updates(cls, user):
        id = user.id
        user.last_active = datetime.datetime.now() # update last login
        DBSession.flush()
        transaction.commit()
        return Users.by(id).first()
        
    @classmethod
    def add_groups(cls, user, groups):
        id = user.id
        user.groups = list(set( (user.groups + groups) ))
        DBSession.flush()
        transaction.commit()
        return Users.by(id).first()
        
    def get_groups(self,field=None):
        from quizsmith.app.models import Groups
        if field:
            z = zip(*DBSession.query(getattr(Groups,field)).join(Users.groups).filter(Users.id==self.id).all())
            if z:
                return list(z.pop())
            return []
        return DBSession.query(Groups).join(Users.groups).filter(Users.id==self.id).all()
        
    @property
    def my_groups(self):
        return self.get_groups()
        
    def _set_password(self, password):
        if password == None:
            self.password = None
        else: 
            hashed_password = password

            if isinstance(password, unicode):
                password_8bit = password.encode('UTF-8')
            else:
                password_8bit = password

            salt = sha1()
            salt.update(os.urandom(60))
            hash = sha1()
            hash.update(password_8bit + salt.hexdigest())
            hashed_password = salt.hexdigest() + hash.hexdigest()

            if not isinstance(hashed_password, unicode):
                hashed_password = hashed_password.decode('UTF-8')
            self.password = hashed_password

    def validate_password(self, password):
        hashed_pass = sha1()
        hashed_pass.update(password + self.password[:40])
        return self.password[40:] == hashed_pass.hexdigest() and self.is_local and self.password != None

    def show_d2l_options(self):
        return (not self.is_local)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    