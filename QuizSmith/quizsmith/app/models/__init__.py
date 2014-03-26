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

from pyramid.httpexceptions import HTTPFound,HTTPForbidden
from sqlalchemy import Table,Integer,Unicode,ForeignKey,Text,Boolean
from sqlalchemy.orm import backref, relation, scoped_session, sessionmaker
from formalchemy import Column, fields
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from zope.sqlalchemy import ZopeTransactionExtension
import transaction

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class AssociatedGroup(object):
    """ M2M Assocation Table handles schema setup """
    
    @declared_attr
    def groups_id(cls):
        return Column(Integer, ForeignKey('groups.id'), primary_key=True)
    
    @declared_attr
    def groups(cls):
        return relation("Groups", backref=backref("Groups",cascade="all,delete-orphan"))
        
    play = Column(Boolean)
    edit = Column(Boolean)
    review = Column(Boolean)

    def __init__(self, id, groups_id, play=False, edit=False, review=False):
        self.associated_table_id = id
        self.groups_id = groups_id
        self.play = play
        self.edit = edit
        self.review = review

        
class GroupAwareModel(object):

    association_with = None

    @property
    def groups(self):
        raise Exception('Must have secondary table declared called "groups"')

    def get_groups(self,field=None):
        from quizsmith.app.models import Groups
        if field:
            z = zip(*DBSession.query(getattr(Groups,field)).join(self.__class__.groups).filter(self.__class__.id==self.id).all())
            if z:
                return list(z.pop())
            return []
        return DBSession.query(Groups).join(self.__class__.groups).filter(self.__class__.id==self.id).all()

    def set_groups(self, players, editors, reviewers):
        from quizsmith.app.models import Groups
        for g in self.groups:
            DBSession.delete(g)
        DBSession.flush()
        for group in Groups.all():
            play = (str(group.id) in players) 
            edit = (str(group.id) in editors)
            review = (str(group.id) in reviewers)
            if group.id == 1 or group.id == 2: # Admin and Global Editors always get full permissions
                self.groups.append(self.association_with(self.id, group.id, play=True, edit=True))
            elif edit or play or review: # Handle rest
                self.groups.append(self.association_with(self.id, group.id, play=play, edit=edit, review=review))
        
class TriviaModel(object):

    @classmethod
    def secure_query(cls, kwargs):
        user = kwargs.get('user',None)
        permission = kwargs.get('permission',None)
        if user and permission:
            if GroupAwareModel in cls.__bases__:
                from quizsmith.app.utilities import ACL
                if permission == ACL.PLAY:
                    return DBSession.query(cls).join(cls.association_with).filter(cls.association_with.groups_id.in_(user.get_groups(field='id'))).filter(cls.association_with.play==True)
                elif permission == ACL.EDIT:
                    return DBSession.query(cls).join(cls.association_with).filter(cls.association_with.groups_id.in_(user.get_groups(field='id'))).filter(cls.association_with.edit==True)
                elif permission == ACL.REVIEW:
                    return DBSession.query(cls).join(cls.association_with).filter(cls.association_with.groups_id.in_(user.get_groups(field='id'))).filter(cls.association_with.review==True)
                return None
            else:
                raise Exception('This is not a GroupAware data Model')
        return DBSession.query(cls)
        
    @classmethod
    def all(cls, **kwargs):
        return cls.secure_query(kwargs).all()

    @classmethod
    def newest(cls, **kwargs):
        order = kwargs.get('sort', 'id desc')
        return  cls.secure_query(kwargs).order_by(order).first() 
        
    @classmethod
    def by(cls, data, **kwargs):
        q = cls.secure_query(kwargs)
        if isinstance(data, dict):
            for k,v in data.iteritems():
                q = q.filter(getattr(cls,k)==v)
        elif data:
            q = q.filter(getattr(cls,'id')==data)
        if kwargs.get('sort',None):
            q = q.order_by(kwargs.get('sort'))
        if kwargs.get('strict', False):
            if not q.count(): # costly, don't do unless strict is on
                print "QUERY STRICT ERROR"
                raise HTTPForbidden() # secure query failed with strict restrictions on
        return q
  

# Make sure to declare interal package shortcuts at end of file.
from quizsmith.app.models.properties import Properties
from quizsmith.app.models.users import Users, UsersGroups
from quizsmith.app.models.groups import Groups, GroupsAssignments
from quizsmith.app.models.categories import Categories
from quizsmith.app.models.questionsets import QuestionSets
from quizsmith.app.models.questions import Questions
from quizsmith.app.models.answers import Answers
from quizsmith.app.models.transitions import Transitions
from quizsmith.app.models.tests import Tests
from quizsmith.app.models.testsresults import TestsResults

