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

from pyramid.httpexceptions import HTTPFound,HTTPForbidden
from pyramid.view import view_config
from quizsmith.app.models import DBSession,Categories,QuestionSets,Questions,Answers,Transitions
from quizsmith.app.utilities import ACL,Validate
from quizsmith.admin import EditBaseView

import transaction

class EditView(EditBaseView):

    @view_config(route_name='edit_question', permission=ACL.EDIT)
    def edit_question(self):
        self.response['category'] = self.request.matchdict['category']
        Categories.by(self.response['category'], user=self.request.user, permission=ACL.EDIT, strict=True).first() # security
        question = self.request.matchdict['id']
        self.response['option'] = question
        
        if question == 'new':
            if 'form.submit' in self.request.params or 'form.submit.next' in self.request.params:
                qs = QuestionSets(category_id=int(self.response['category']))
                DBSession.add(qs)
                DBSession.flush()
                qs = QuestionSets.by(None, sort='id desc').first()
                id = qs.id
                self._transaction(qs, self.request.params)
                if 'form.submit.next' in self.request.params:
                    return HTTPFound(location=self.request.application_url + self.request.path)
                return HTTPFound(location=self.request.application_url + self.request.path + '/../' + str(id))
        else:
            qs = QuestionSets.by(question).first()
            q = Questions.by({'question_sets_id':qs.id}).all()
            wa = Answers.by({'question_sets_id':qs.id,'is_correct':False}, sort='position asc').all()
            ca = Answers.by({'question_sets_id':qs.id,'is_correct':True}).first()
            self.response['question_sets'] = qs
            self.response['questions'] = q
            self.response['wrong_answers'] = wa
            self.response['correct_answer'] = ca
            if 'form.submit' in self.request.params or 'form.submit.next' in self.request.params:
                self._transaction(qs, self.request.params)
                if 'form.submit.next' in self.request.params:
                    return HTTPFound(location=self.request.application_url + self.request.path + '/../new')
                return HTTPFound(location=self.request.application_url + self.request.path)
        
        return self.template('/edit-question.pt', theme='AdminPanel')

        

    def _transaction(self, question_set, fields):
         
        for key,v in fields.iteritems():
            if Validate.sanatize(v) != '':
               
                parts = key.split('_')
            
                if parts[0] == 'answerhelp':
                    question_set.answer_help = v

                if parts[0] == 'correctanswer' and not key.endswith('_index'):
                    if parts[1] == 'old':
                        a = Answers.by(parts[2]).first()
                        a.answer = v
                        a.position=fields[key + '_index']
                    else:
                        a = Answers(question_sets_id=question_set.id, answer=v, is_correct=True, position=fields[key + '_index'])
                        DBSession.add(a)
                
                if parts[0] == 'wronganswer' and not key.endswith('_index'):
                    if parts[1] == 'old':
                        a = Answers.by(parts[2]).first()
                        a.answer = v
                        a.position = fields[key + '_index']
                    else:
                        a = Answers(question_sets_id=question_set.id, answer=v, is_correct=False, position=fields[key + '_index'])
                        DBSession.add(a)
                        
                if parts[0] == 'question':
                    if parts[1] == 'old':
                        a = Questions.by(parts[2]).first()
                        a.question = v
                    else:
                        a = Questions(question=v, question_sets_id=question_set.id)
                        DBSession.add(a)
        
            DBSession.flush()
        transaction.commit()
        
        
        
        
        
        
        
        
        
        