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

from sqlalchemy import Integer,ForeignKey,Float,Unicode,Boolean,Text,and_
from sqlalchemy.orm import backref, relation
from formalchemy import Column, fields
from fa.jquery import renderers
from quizsmith.app.models import Base,DBSession,TriviaModel
import json

class TestsResults(Base, TriviaModel):
    __tablename__ = 'tests_results'
    __label__ = 'Test Result' # fa scaffold
    __plural__ = 'Tests Results' # fa scaffold
    
    id = Column(Integer, primary_key=True, label='Result ID')
    tests_id = Column(Integer, ForeignKey('tests.id'), label='Test', renderer=fields.SelectFieldRenderer, readonly=True)
    tests = relation('Tests')
    question_sets_id = Column(Integer, label='Question Set' , readonly=True)
    question = Column(Text, label='Question', readonly=True) 
    correctly_answered = Column(Boolean, label='Correctly Answered', readonly=True)
    wrong_attempts = Column(Integer, label='Wrong Attempts', size=80, readonly=True)
    duration = Column(Float, label='Duration (ms?)', size=80, readonly=True)
    answer_choices = Column(Text, label='JSON Answer Choices', size=80, readonly=True)
    attempted = Column(Boolean, label='Attempted', readonly=True)
    
    def __init__(self,**kwargs):
        self.tests_id = kwargs.get('tests_id',0)
        self.question_sets_id = kwargs.get('question_sets_id',0)
        self.question = kwargs.get('question','')
        self.correctly_answered = kwargs.get('correctly_answered',False)
        self.wrong_attempts = kwargs.get('wrong_attempts',0)
        self.duration = kwargs.get('duration',0)
        self.attempted = kwargs.get('attempted',False)
        self.set_answers(kwargs.get('answer_choices',"[]"))
        
    def __unicode__(self):
        return unicode(self.question)
     
    def set_answers(self,dictionary):
        self.answer_choices = json.dumps(dictionary)
    
    def get_answers(self):
        if self.answer_choices:
            return json.loads(self.answer_choices)
        return ""
    