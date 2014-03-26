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

from operator import itemgetter
from sqlalchemy import Table,Integer,Unicode,ForeignKey,Text,Boolean,TIMESTAMP
from sqlalchemy.orm import backref, relation
from formalchemy import Column, fields
from sqlalchemy.ext.declarative import declared_attr
from fa.jquery import renderers
from quizsmith.app.models import Base, DBSession, TriviaModel, GroupAwareModel, AssociatedGroup
import datetime,json

class CategoriesLocalizedGroups(AssociatedGroup,Base):
    __tablename__ = 'categories_local_groups'
    associated_table_id = Column(Integer, ForeignKey('categories.id'), primary_key=True)
    categories = relation("Categories", backref=backref("Categories"))

    
class Categories(Base, TriviaModel, GroupAwareModel):
    __tablename__ = 'categories'
    __label__ = 'Category' # fa scaffold
    __plural__ = 'Categories' # fa scaffold
    
    id = Column(Integer, primary_key=True, label='Category ID')
    name = Column(Unicode(55), label='Category Name')
    category_intro = Column(Text, label='Intro', renderer=renderers.RichTextFieldRenderer(use='tinymce'))
    playable_questions = Column(Integer(11), label='Playable Questions')
    wrong_answer_time_penalty = Column(Integer(11), label='Wrong Answer Time Penalty')
    max_wrong_answer_allowed = Column(Integer(11), label='Max Wrong Answers Allowed')
    question_time_allowed = Column(Integer(11), label='Question Time Limit')
    
    transition_in = Column(Integer, ForeignKey('transitions.id'), label='Transition In', renderer=fields.SelectFieldRenderer)
    transitions_in = relation('Transitions',primaryjoin='Categories.transition_in==Transitions.id')
    transition_out = Column(Integer, ForeignKey('transitions.id'), label='Transition Out', renderer=fields.SelectFieldRenderer)
    transitions_out = relation('Transitions',primaryjoin='Categories.transition_out==Transitions.id')
    
    position = Column(Integer, label='Position')
    can_anonymous_view_intro = Column(Boolean, label='Is Public?')
    
    d2l_folder = Column(Unicode(55), label='D2L Folder Name')
    assessments = Column(Text, label='Assessments', size=80, readonly=True)
    
    created = Column(TIMESTAMP, default=datetime.datetime.now())
    modified = Column(TIMESTAMP, default=datetime.datetime.now())
    
    groups = relation("CategoriesLocalizedGroups", cascade="all, delete")
    association_with = CategoriesLocalizedGroups
  
    def __init__(self, **kwargs):
        self.name = kwargs.get('name','New Category')
        self.category_intro = kwargs.get('category_intro','Your intro here')
        self.playable_questions = kwargs.get('playable_questions',10)
        self.wrong_answer_time_penalty = kwargs.get('wrong_answer_time_penalty',15)
        self.max_wrong_answer_allowed = kwargs.get('max_wrong_answer_allowed',2)
        self.question_time_allowed = kwargs.get('question_time_allowed',30)
        self.transition_in = kwargs.get('transition_in',1)
        self.transition_out = kwargs.get('transition_out',1)
        self.position = kwargs.get('position',99)
        self.can_anonymous_view_intro = kwargs.get('can_anonymous_view_intro', False)
        self.groups = []
        self.d2l_folder = kwargs.get('d2l_folder', '')
        self.set_assessments([])
        self.created = datetime.datetime.now()
        
    def __unicode__(self):
        return unicode(self.name)

    def get_transition_in(self):
        from quizsmith.app.models import Transitions
        return DBSession.query(Transitions).join(Categories.transitions_in).filter(Categories.id==self.id).first()
        
    def get_transition_out(self):
        from quizsmith.app.models import Transitions
        return DBSession.query(Transitions).join(Categories.transitions_out).filter(Categories.id==self.id).first()
        
    def set_assessments(self,data):
        if data:
            data = sorted(data, key=itemgetter('end'), reverse=True)
        self.assessments = json.dumps(data)
    
    @property
    def get_assessments(self):
        if self.assessments:
            return json.loads(self.assessments)
        return []
        
    def assess_this(self,score):
        range = filter(lambda x: x['start'] <= score and x['end'] >= score, self.get_assessments)
        if not range:
            return {'start':-1,'end':-1,'text':'No assessment range has be sent'}
        return range[0]
        
        