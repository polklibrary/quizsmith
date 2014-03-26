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

from sqlalchemy import Integer,Unicode
from sqlalchemy.orm import backref, relation
from formalchemy import Column
from quizsmith.app.models import Base,DBSession,TriviaModel

class Transitions(Base,TriviaModel):
    __tablename__ = 'transitions'
    __label__ = 'Transition' # fa scaffold
    __plural__ = 'Transitions' # fa scaffold
    
    id = Column(Integer, primary_key=True, label='Transition ID')
    name = Column(Unicode(55), label='Transition Type', readonly=True)
  
    def __init__(self):
       pass
       
    def __unicode__(self):
        return unicode(self.name)
        