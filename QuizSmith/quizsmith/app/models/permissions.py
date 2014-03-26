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
from sqlalchemy.orm import relation
from formalchemy import Column, fields
from fa.jquery import renderers
from quizsmith.app.models import Base,TriviaModel

class Permissions(Base, TriviaModel):
    __tablename__ = 'permissions'
    __label__ = 'Permission' # fa scaffold
    __plural__ = 'Permissions' # fa scaffold
    
    id = Column(Integer, primary_key=True, label='Permission ID')
    name = Column(Unicode(25), unique=True, label='Permission', renderer=fields.TextFieldRenderer, readonly=True)
    description = Column(Unicode(55), unique=True, label='Permission Description', readonly=True)
   
    def __init__(self, **kwargs):
        self.name = kwargs.get('name','')
        self.description = kwargs.get('description','')
        
    def __unicode__(self):
        return unicode(self.name)
