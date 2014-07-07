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
from pyramid.url import route_url
from pyramid.view import view_config
from quizsmith.app.models import Users
from quizsmith.app.views import BaseView
from quizsmith.app.utilities import ACL,Validate

import transaction

class Alias(BaseView):

    @view_config(route_name='alias', permission=ACL.AUTHENTICATED)
    def alias(self):
        if self.request.user.alias:
            return self.reroute()

        self.response['alias'] =  ''
        self.response['category'] = self.request.params.get('category','0')
        self.response['accessibility'] = False
        if 'form.submitted' in self.request.params:
            self.response['alias'] = Validate.sanatize(self.request.params['alias'])
            self.response['accessibility'] = Validate.bool(self.request.params.get('accessibility', False))

            user = Users.by({'alias':self.response['alias']}).first()
            if user:
                self.notify('Alias already in use!',warn=True)
            elif not Validate.alias(self.response['alias']):
                self.notify('Improper alias!',warn=True)
            else:
                user = Users.by(self.request.user.id).first()
                user.alias = self.response['alias']
                user.needs_accessibility = self.response['accessibility']
                transaction.commit()
                return self.reroute()
                
        return self.template('alias.pt')
        
    def reroute(self):
        """ Reroute the user if a category is defined. """ 
        if int(self.request.params.get('category', '0')) > 0:
            return HTTPFound(location=route_url('category_intro', self.request, id=self.request.params['category'] ))
        else:
            return HTTPFound(location=route_url('category', self.request))
        
        