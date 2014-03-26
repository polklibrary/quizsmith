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

from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from pyramid.url import route_url
from quizsmith.app.views import BaseView
from quizsmith.app.utilities import ACL,Seconds2Str
from quizsmith.app.models import Tests

class Profile(BaseView):

    @view_config(route_name='profile', permission=ACL.AUTHENTICATED)
    def profile(self):
        self.response['played'] = True
        self.response['category'] = 0
        self.response['tests'] = []
        self.response['categories'] = []
        
        self.response['format_time'] = Seconds2Str
        
        try:
            if 'category' in self.request.params:
                self.response['category'] = self.request.params['category']
                self.response['tests'] = Tests.by({'category':self.response['category'], 'alias':self.request.user.alias}, sort='id desc').all()
            else:
                self.response['categories'] = Tests.best_by_user_alias(self.request.user.alias)
        except:
            self.response['played'] = False
            
        return self.template('profile.pt')

        
        
        
        