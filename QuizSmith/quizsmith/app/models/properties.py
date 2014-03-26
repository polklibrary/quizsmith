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

from sqlalchemy import Integer,ForeignKey,Unicode
from sqlalchemy.orm import backref, relation
from formalchemy import Column, fields
from fa.jquery import renderers
from quizsmith.app.models import Base,DBSession,TriviaModel


class Properties(Base,TriviaModel):
    __tablename__ = 'properties'
    __label__ = 'Property' # fa scaffold
    __plural__ = 'Properties' # fa scaffold
    
    id = Column(Integer, primary_key=True, label='Property ID')
    prop_name = Column(Unicode(255), label='Name', size=80)
    prop_value = Column(Unicode(255), label='Value', size=80)
    
    def __init__(self, **kwargs):
        self.prop_name = kwargs.get('prop_name','')
        self.prop_value = kwargs.get('prop_value','')
        
    def __unicode__(self):
        return self.prop_name

    @classmethod
    def get(cls,name,default=None):
        try:
            prop = DBSession.query(Properties).filter(Properties.prop_name==name).first().prop_value
            if prop:
                return prop
            return default
        except:
            return default
            
    @classmethod
    def all_properties(cls):
        results = DBSession.query(Properties).all()
        properties = {}
        for result in results:
            properties[result.prop_name] = result.prop_value
        return properties