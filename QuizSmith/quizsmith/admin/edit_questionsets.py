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
from quizsmith.app.utilities import ACL
from quizsmith.admin import EditBaseView

import transaction

class EditView(EditBaseView):
        
    @view_config(route_name='edit_questions', permission=ACL.EDIT)
    def edit_questions(self):
        category = self.request.matchdict['category']
        self.response['active_category'] = Categories.by(category, user=self.request.user, permission=ACL.EDIT, strict=True).first()
        question_sets = QuestionSets.by({'category_id':category}).all()
        
        self.response['question_sets'] = []
        i = 1
        for qs in question_sets:
            self.response['question_sets'].append({
                'rank' : i,
                'id' : qs.id,
                'answer_help' : qs.answer_help,
                'questions' : Questions.by({'question_sets_id':qs.id}).all(),
                'wrong_answers' : Answers.by({'question_sets_id':qs.id,'is_correct':False}).all(),
                'correct_answer' : Answers.by({'question_sets_id':qs.id,'is_correct':True}).first(),
            })
            i += 1
        return self.template('/edit-questions.pt', theme='AdminPanel')

        
        
        
        
        
        
        
        
        
        
        
        