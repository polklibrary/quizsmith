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

from sqlalchemy import Integer,Unicode,ForeignKey,Boolean,Table
from sqlalchemy.orm import relation
from formalchemy import Column, fields
from fa.jquery import renderers
from quizsmith.app.models import Base,DBSession,Properties,TriviaModel

GroupsAssignments = Table('groups_assignments', Base.metadata,
    Column('groups_id', Integer, ForeignKey('groups.id'), primary_key=True),
    Column('categories_id', Integer, ForeignKey('categories.id'), primary_key=True),
)

class Groups(Base, TriviaModel):
    __tablename__ = 'groups'
    __label__ = 'Group' # fa scaffold
    __plural__ = 'Groups' # fa scaffold
    
    id = Column(Integer, primary_key=True, label='Group ID')
    name = Column(Unicode(25), unique=True, label='Group Name')
    description = Column(Unicode(55), unique=True, label='Group Description')
    play =  Column(Boolean, label='General Play Permission')
    edit =  Column(Boolean, label='General Edit Permission')
    review =  Column(Boolean, label='General Review Permission')
    use_admin_panel =  Column(Boolean, label='General Admin Permission')
    categories = relation('Categories', secondary='groups_assignments')
    
    
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', 'New Group')
        self.description = kwargs.get('description', 'Group Description')
        self.play = kwargs.get('play', False)
        self.edit = kwargs.get('edit', False)
        self.review = kwargs.get('review', False)
        self.use_admin_panel = kwargs.get('use_admin_panel', False)
        self.categories = []
    
    @classmethod
    def groups_auto_assigned_by_category(self,category_id):
        from quizsmith.app.models import Categories
        return DBSession.query(Groups).join(Groups.categories).filter(Categories.id==category_id).all()
        
    def __unicode__(self):
        return unicode(self.name)
    
    def permissions(self,is_list=False):
        from quizsmith.app.utilities import ACL
        allowed = [ACL.AUTHENTICATED]
        if self.play:
            allowed.append(ACL.PLAY)
        if self.edit:
            allowed.append(ACL.EDIT)
        if self.review:
            allowed.append(ACL.REVIEW)
        if self.use_admin_panel:
            allowed.append(ACL.ADMIN)
        if not is_list:
            return tuple(allowed)
        return allowed
   