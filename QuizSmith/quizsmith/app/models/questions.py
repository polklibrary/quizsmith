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

from sqlalchemy import Integer,ForeignKey,Unicode,Text
from sqlalchemy.orm import backref, relation
from formalchemy import Column, fields
from fa.jquery import renderers
from quizsmith.app.models import Base,DBSession,TriviaModel

class Questions(Base, TriviaModel):
    __tablename__ = 'questions'
    __label__ = 'Question' # fa scaffold
    __plural__ = 'Questions' # fa scaffold
    
    id = Column(Integer, primary_key=True, label='Question ID')
    question = Column(Text, label='Question', renderer=renderers.RichTextFieldRenderer(use='tinymce'))
    question_sets_id = Column(Integer, ForeignKey('question_sets.id'), label='QuestionSet ID', renderer=fields.SelectFieldRenderer)
    
    
    def __init__(self,**kwargs):
        self.question = kwargs.get('question','')
        self.question_sets_id = kwargs.get('question_sets_id','0')
        
    def __unicode__(self):
        return unicode(self.question)
        