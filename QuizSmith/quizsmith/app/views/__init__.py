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
from quizsmith.app.models import Users, Properties
import pkg_resources,os

class BaseView(object):

    def __init__(self, request):
        self.request = request
        self.context = request.context
        self.theme = self.request.active_base_theme
        self.response = {'instance_id' : 'default',
                         'analytics' : Properties.get('ANALYTICS')}
    
    def notify(self, message, warn=False):
        lvl = 'info'
        if warn:
            lvl = 'warn'
        self.request.session.flash({'content':message,'lvl':lvl})
    
    def log_if_error(self,line):
        """ This will not log unless an error happens """
        self.request.errors += str(line) + '\n' 
    
    def determine_instance(self,theme):
        if theme:
            self.theme = theme
        if self.theme:
            theme_dir = pkg_resources.resource_filename('quizsmith', 'themes/' + self.settings('theme.folder','default'))
            os.chdir(theme_dir)
            folders = [d for d in os.listdir('.') if os.path.isdir(d)]
            if self.theme not in folders:
                self.response['instance_id'] = 'default'
            else:
                self.response['instance_id'] = self.settings('theme.folder','default')
        else:
            self.response['instance_id'] = self.settings('theme.folder','default')
        
    def settings(self,name,default=None):
        try:
            return self.request.registry.settings[name]
        except:
            return default
        
    def template(self, template, content_type='text/html', backup='../../', status=None, theme=''):
        """ Template renderer for dynamic themes """
        try:
            self.determine_instance(theme)
            response  = Response(content_type=content_type, status=status)
            response.text = render(backup + 'themes/' + self.response['instance_id'] + '/' + self.theme + '/templates/' + template, self.response, self.request)
            return response
        except Exception as e:
            print "ERROR: " + str(e)
            raise HTTPForbidden()
            