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

from sqlalchemy import Integer,ForeignKey,Unicode,Text,TIMESTAMP,Table,and_
from sqlalchemy.orm import backref, relation
from formalchemy import Column, fields
from fa.jquery import renderers
from quizsmith.app.models import Base,DBSession,TriviaModel
import datetime

class QuestionSets(Base, TriviaModel):
    __tablename__ = 'question_sets'
    __label__ = 'Question Set' # fa scaffold
    __plural__ = 'Question Sets' # fa scaffold
    
    id = Column(Integer, primary_key=True, label='Question Set ID')
    category_id = Column(Integer, ForeignKey('categories.id'), label='Category', renderer=fields.SelectFieldRenderer)
    categories = relation('Categories')
    questions = relation('Questions', cascade="all, delete")
    answer_help = Column(Text, label='Answer Help', renderer=renderers.RichTextFieldRenderer(use='tinymce'))
    created = Column(TIMESTAMP, default=datetime.datetime.now())
    modified = Column(TIMESTAMP, default=datetime.datetime.now())
    
    def __init__(self,**kwargs):
        self.category_id =  kwargs.get('category_id',0)
        self.answer_help = kwargs.get('answer_help','')
        self.created = datetime.datetime.now()
        
    def __unicode__(self):
        return unicode(self.id)
