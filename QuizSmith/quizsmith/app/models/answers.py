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

from sqlalchemy import Integer,ForeignKey,Unicode,Boolean
from sqlalchemy.orm import backref, relation
from formalchemy import Column, fields
from fa.jquery import renderers
from quizsmith.app.models import Base,DBSession,TriviaModel


class Answers(Base, TriviaModel):
    __tablename__ = 'answers'
    __label__ = 'Answer' # fa scaffold
    __plural__ = 'Answers' # fa scaffold
    
    id = Column(Integer, primary_key=True, label='Wrong Answers')
    question_sets_id = Column(Integer, ForeignKey('question_sets.id'), label='Question Set', renderer=fields.SelectFieldRenderer)
    answer = Column(Unicode(255), label='Answer', size=80)
    is_correct = Column(Boolean, label='Is Correct Answer')
    position = Column(Integer, label='Position? If all 0 all random.')
    
    def __init__(self,**kwargs):
        self.question_sets_id = kwargs.get('question_sets_id',0)
        self.answer = kwargs.get('answer','')
        self.is_correct = kwargs.get('is_correct',False)
        self.position = kwargs.get('position',0)
        
    def __unicode__(self):
        return unicode(self.answer)
        