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

from operator import itemgetter
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from pyramid.url import route_url
from quizsmith.admin.edit_reports import Reports
from quizsmith.admin import EditBaseView
from quizsmith.app.models import DBSession,Categories,QuestionSets,Tests,TestsResults
from quizsmith.app.utilities import ACL,Validate

import ast

class EditView(EditBaseView):

    @view_config(route_name='edit_report_avg_score', permission=ACL.EDIT)
    def edit_report_avg_score(self):
        if 'form.submit' not in self.request.params:
            return HTTPFound(location=route_url('edit_reports', self.request))

        self.response = ImprovementOvertime(self.request, self.response).run()
        return self.template('/edit-reports-avg-score.pt', theme='AdminPanel')

        
class ImprovementOvertime(Reports):

    def run(self):
        category = self.request.params.get('category','missing')
        
        attempts = {} #'THE_USER_NAME_HERE':1
        questions = []
        
        tests = DBSession.query(Tests).filter(Tests.category==category).filter(Tests.created>=self.start).filter(Tests.created<=self.end).order_by('created asc')
        if not self.include_incompleted:
            tests = tests.filter(Tests.completed==1)
        tests = tests.all()
        
        data = [
            {'Attempt':'1st Attempt', 'Score':0, 'Of':0},
            {'Attempt':'2nd Attempt', 'Score':0, 'Of':0},
            {'Attempt':'3rd Attempt', 'Score':0, 'Of':0},
            {'Attempt':'4th Attempt', 'Score':0, 'Of':0},
            {'Attempt':'5th Attempt', 'Score':0, 'Of':0}
        ]
        
        for test in tests:
            if not test.alias in attempts:
                attempts[test.alias] = 0
            else:
                attempts[test.alias] += 1
            
            outof = DBSession.query(TestsResults).filter(TestsResults.tests_id==test.id).count()
            percent = test.total_percentage / outof
            
            if attempts[test.alias] < 5:
                data[attempts[test.alias]]['Score'] += percent
                data[attempts[test.alias]]['Of'] += 1
                
        for i in range(5):
            if data[i]['Of'] > 0:
                data[i]['Score'] = float(data[i]['Score'] / data[i]['Of'])
                data[i]['Attempt'] += ' : ' + str(data[i]['Of']) + ' users '
        
        self.response['dataset'] = data
        return self.response
        

        
        