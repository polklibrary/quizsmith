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

from sqlalchemy import Integer,Float,ForeignKey,Unicode,Boolean,TIMESTAMP,and_,desc,func
from sqlalchemy.orm import backref, relation
from formalchemy import Column, fields
from fa.jquery import renderers
from quizsmith.app.models import Base,DBSession,TriviaModel
import datetime

class Tests(Base, TriviaModel):
    __tablename__ = 'tests'
    __label__ = 'Test' # fa scaffold
    __plural__ = 'Tests' # fa scaffold
    
    id = Column(Integer, primary_key=True, label='Test ID')
    alias = Column(Unicode(25), label='Player Alias')
    category = Column(Unicode(255), label='Category')
    d2l_folder = Column(Unicode(255), label='Category')
    completed = Column(Boolean, label='Completed', readonly=True)
    total_percentage = Column(Float, label='Percentage')
    base_competitive = Column(Integer, label='Competitive Base')
    bonus_competitive = Column(Integer, label='Competitive Bonus')
    total_competitive = Column(Integer, label='Competitive Total')
    time_remaining = Column(Float, label='Total Time Remaining')
    time_spent = Column(Float, label='Total Time Spent')
    wrong_answer_time_penalty = Column(Integer(11), label='Wrong Answer Time Penalty')
    max_wrong_answer_allowed = Column(Integer(11), label='Max Wrong Answers Allowed')
    question_time_allowed = Column(Integer(11), label='Question Time Limit')
    used_accessibility_view = Column(Boolean, label='Used Accessibility View', readonly=True)
    created = Column(TIMESTAMP, default=datetime.datetime.now())
    modified = Column(TIMESTAMP, default=datetime.datetime.now())
    
    
    def __init__(self, **kwargs):
        self.alias = kwargs.get('alias','{unknown}')
        self.category = kwargs.get('category','')
        self.d2l_folder = kwargs.get('d2l_folder','')
        self.completed = kwargs.get('completed',False)
        self.total_percentage = kwargs.get('total_percentage',0.0)
        self.total_competitive = kwargs.get('total_competitive',0)
        self.base_competitive = kwargs.get('base_competitive',0)
        self.bonus_competitive = kwargs.get('bonus_competitive',0)
        self.time_remaining = kwargs.get('time_remaining',0.0)
        self.time_spent = kwargs.get('time_spent',0.0)
        self.wrong_answer_time_penalty = kwargs.get('wrong_answer_time_penalty',0.0)
        self.max_wrong_answer_allowed = kwargs.get('max_wrong_answer_allowed',0.0)
        self.question_time_allowed = kwargs.get('question_time_allowed',0.0)
        self.used_accessibility_view = kwargs.get('used_accessibility_view',False)
        self.created = datetime.datetime.now()
        
    def __unicode__(self):
        return unicode(self.category)
    
    @property
    def total_time(self):
        d = self.modified - self.created
        return d.seconds 
    
    @property
    def percentage(self):
        from quizsmith.app.models import TestsResults
        count = TestsResults.by({'tests_id':self.id}).count()
        return round((self.total_percentage / count), 1)

    @classmethod
    def best_by_user_alias(cls,alias):
        from quizsmith.app.models import TestsResults
        from quizsmith.app.utilities import Seconds2Str
        tests = DBSession.query(Tests,func.count(Tests.category)).filter(Tests.alias==alias).group_by(Tests.category).all()

        results = []
        for test in tests:
            best_duration = DBSession.query(Tests).filter(Tests.alias==alias).filter(Tests.category==test[0].category).filter(Tests.time_spent > 0).order_by('time_spent asc').first().time_spent
            best_scores = DBSession.query(Tests).filter(Tests.alias==alias).filter(Tests.category==test[0].category).order_by('total_competitive desc').first()
            last_played = DBSession.query(Tests).filter(Tests.alias==alias).filter(Tests.category==test[0].category).order_by('created desc').first().created
            results.append({'Test':test[0], 
                            'best_duration':Seconds2Str(best_duration), 
                            'best_percentage':round(best_scores.percentage,2), 
                            'best_competitive':int(best_scores.total_competitive), 
                            'Count':test[1], 
                            'last_played': last_played.strftime('%m/%d/%Y %I:%M %p')})
        return results
        

        
        
        
        
        
        
        
        
        
        
        