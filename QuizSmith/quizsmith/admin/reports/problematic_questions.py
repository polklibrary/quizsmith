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

import ast, json

class EditView(EditBaseView):

    @view_config(route_name='edit_reports_problematic_questions', permission=ACL.EDIT)
    def edit_reports_problematic_questions(self):
        if 'form.submit' not in self.request.params:
            return HTTPFound(location=route_url('edit_reports', self.request))
        
        self.response['rows'] = []
        self.response = ProblematicQuestions(self.request, self.response).run()
        return self.template('/edit-reports-problematic-questions.pt', theme='AdminPanel')

        
class ProblematicQuestions(Reports):

    def run(self):
        category = self.request.params.get('category','missing')
        
        attempts = {} # { 'KEY_USER_NAME' : INT_ATTEMPT_COUNT }
        questions = []
        
        tests = DBSession.query(Tests).filter(Tests.category==category).filter(Tests.created>=self.start).filter(Tests.created<=self.end).order_by('created asc')
        if not self.include_incompleted:
            tests = tests.filter(Tests.completed==1)
        tests = tests.all()
        
        for test in tests:
            if not test.alias in attempts:
                attempts[test.alias] = 1
            else:
                attempts[test.alias] += 1
            
            results = DBSession.query(TestsResults).filter(TestsResults.tests_id==test.id).all()
            for result in results:
                
                data = None
                for ds in questions:
                    if ds.equals(result.question):
                        data = ds
                if data == None:
                    data = self.Struct(result.question, result.question_sets_id)
                    data.wrong_multiplier = test.max_wrong_answer_allowed
                    questions.append(data)
                
                if attempts[test.alias] == 1:
                    if result.wrong_attempts != 0:
                        if result.wrong_attempts == test.max_wrong_answer_allowed:
                            data.attempts_one_wrong += 1
                        else:
                            data.attempts_one_partial += 1
                        data.wrongly_answered(result.answer_choices, data.answer_one_choices)
                    else:
                        data.attempts_one_correct += 1
                    
                if attempts[test.alias] == 2:
                    if result.wrong_attempts != 0:
                        if result.wrong_attempts == test.max_wrong_answer_allowed:
                            data.attempts_two_wrong += 1
                        else:
                            data.attempts_two_partial += 1
                        data.wrongly_answered(result.answer_choices, data.answer_two_choices)
                    else:
                        data.attempts_two_correct += 1
                        
                if attempts[test.alias] == 3:
                    if result.wrong_attempts != 0:
                        if result.wrong_attempts == test.max_wrong_answer_allowed:
                            data.attempts_three_wrong += 1
                        else:
                            data.attempts_three_partial += 1
                        data.wrongly_answered(result.answer_choices, data.answer_three_choices)
                    else:
                        data.attempts_three_correct += 1
                    
        for question in questions:
            data = {}
            data['question'] = question.question
            data['question_sets_id'] = str(question.question_sets_id)
            data['wrong_multiplier'] = question.wrong_multiplier
            
            data['one_percent'] = self.percentage(float(question.attempts_one_wrong) / float(question.attempts_one_wrong + question.attempts_one_correct))
            data['one_wrong'] = question.attempts_one_wrong
            data['one_partial'] = question.attempts_one_partial
            data['one_correct'] = question.attempts_one_correct
            data['one_answers'] = filter(lambda x: x['wrong'] != 0, sorted(question.answer_one_choices, key=itemgetter('wrong'), reverse=True))

            data['two_percent'] = self.percentage(float(question.attempts_two_wrong) / float(question.attempts_two_wrong + question.attempts_two_correct))
            data['two_wrong'] = question.attempts_two_wrong
            data['two_partial'] = question.attempts_two_partial
            data['two_correct'] = question.attempts_two_correct
            data['two_answers'] = filter(lambda x: x['wrong'] != 0, sorted(question.answer_two_choices, key=itemgetter('wrong'), reverse=True))

            data['three_percent'] = self.percentage(float(question.attempts_three_wrong) / float(question.attempts_three_wrong + question.attempts_three_correct))
            data['three_wrong'] = question.attempts_three_wrong
            data['three_partial'] = question.attempts_three_partial
            data['three_correct'] = question.attempts_three_correct
            data['three_answers'] = filter(lambda x: x['wrong'] != 0, sorted(question.answer_three_choices, key=itemgetter('wrong'), reverse=True))
            
            self.response['rows'].append(data)
        return self.response
        
        
    class Struct(object):
        """ Simple data structure for this report """
        question = ''
        question_sets_id = ''
        wrong_multiplier = 1
        answer_one_choices = []
        attempts_one_wrong = 0
        attempts_one_partial = 0
        attempts_one_correct = 0
        answer_two_choices = []
        attempts_two_wrong = 0
        attempts_two_partial = 0
        attempts_two_correct = 0
        answer_three_choices = []
        attempts_three_wrong = 0
        attempts_three_partial = 0
        attempts_three_correct = 0
            
        def __init__(self,question,set_id):
            self.question = question
            self.question_sets_id = set_id
            self.answer_one_choices = []
            self.answer_two_choices = []
            self.answer_three_choices = []
        
        def equals(self,question):
            return (self.question == question)
        
        def wrongly_answered(self, choices, group):
            if not choices: return None
            choices = ast.literal_eval(choices)
            if not group:
                for c in choices:
                    group.append({'content': c['content'], 'wrong':0 })
            for ac in group:
                for c in choices:
                    if ac['content'] == c['content'] and c['answered'] == -1:
                        ac['wrong'] += 1
            
        
