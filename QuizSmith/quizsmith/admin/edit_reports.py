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
from quizsmith.app.models import DBSession,Tests
from quizsmith.app.utilities import ACL,Validate
from quizsmith.admin import EditBaseView

import datetime

class EditView(EditBaseView):

    # Match the key with a method in the ReportGenerator
    @view_config(route_name='edit_reports', permission=ACL.EDIT)
    def edit_reports(self):
        self.response['played_categories'] = Tests.by(None, sort='category asc').group_by('category').all()
        return self.template('/edit-reports.pt', theme='AdminPanel')

class Reports(object):

    def __init__(self, request, response):
        self.response = response
        self.request = request
        self.response['category'] = self.request.params.get('category','Unknown Category')
        s = request.params.get('start','').strip(' ')
        if s == '': s = '1/1/2000'
        e = request.params.get('end','').strip(' ')
        if e == '': e = '1/1/2030'
        self.start = datetime.datetime.strptime(s, '%m/%d/%Y')
        self.end = datetime.datetime.strptime(e, '%m/%d/%Y')
        self.include_incompleted = Validate.bool(self.request.params.get('incompleted', False))
        
    def percentage(self, f, show_sign=True):
        p = '{0:.2f}'.format(f*100).rjust(5, '0')
        if show_sign:
            return p + '%'
        return float(p)
        
        
        