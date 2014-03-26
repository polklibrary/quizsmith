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

from pyramid.httpexceptions import HTTPForbidden
from pyramid.security import unauthenticated_userid
from pyramid.response import Response
from pyramid.renderers import render
from quizsmith.app.models import Users

class BaseView(object):

    def __init__(self, request):
        self.request = request
        self.context = request.context
        self.response = {'message' : '' , 'message_class' : 'warn'}
        
    def settings(self,name,default=None):
        try:
            return self.request.registry.settings[name]
        except:
            return default
        
    def template(self, template, content_type='text/html', backup='../../', status=None, theme=''):
        """ Template renderer for dynamic themes """
        try:
            if not theme:
                theme = self.request.active_base_theme
            response  = Response(content_type=content_type, status=status)
            response.text = render(backup + 'themes/' + theme + '/templates/' + template, self.response, self.request)
            return response
        except Exception as e:
            print "ERROR: " + str(e)
            raise HTTPForbidden()