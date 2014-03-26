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
from quizsmith.app.models import DBSession,Categories,Groups,Transitions
from quizsmith.app.utilities import ACL,Validate
from quizsmith.admin import EditBaseView
from quizsmith.setup import Addons

import transaction

class EditView(EditBaseView):

    @view_config(route_name='edit_categories', permission=ACL.EDIT)
    def edit_categories(self):
        if 'form.submit' in self.request.params:
            for k,v in self.request.params.iteritems():
                if k.isdigit():
                    c = Categories.by(k).first()
                    c.position = v;
                    DBSession.flush()
            transaction.commit()
            return HTTPFound(location=self.request.application_url + '/edit')
        return self.template('/edit-categories.pt', theme='AdminPanel')
        
        
    @view_config(route_name='edit_category', permission=ACL.EDIT)
    def edit_category(self):
        category_id = self.request.matchdict['category']
        self.response['category_id'] = category_id
        self.response['version'] = Addons.get_version('QuizSmith Core')
        self.response['d2l_on'] = Validate.bool(self.settings('d2l_on'))
        
        if 'form.submit' in self.request.params or 'form.submit.questions' in self.request.params:
            active = None
            if category_id == 'add':
                active = Categories(name='New Category')
                editors = []
                for group in self.request.user.get_groups():
                    editors.append(str(group.id))
                reviewers = []
                for group in self.request.user.get_groups():
                    reviewers.append(str(group.id))
                active.set_groups([], editors, reviewers)
                DBSession.add(active)
                DBSession.flush()
                category_id = str(active.id)
            else:
                active = Categories.by(category_id, sort='position asc', user=self.request.user, permission=ACL.EDIT).first()
            
            active.name = self.request.params.get('category.name','')
            active.category_intro = self.request.params.get('category.intro','')
            active.playable_questions = self.request.params.get('category.playable_questions',10)
            active.wrong_answer_time_penalty = self.request.params.get('category.wrong_answer_time_penalty',5)
            active.max_wrong_answer_allowed = self.request.params.get('category.max_wrong_answer_allowed',2)
            active.question_time_allowed = self.request.params.get('category.question_time_allowed',30)
            active.transition_in = self.request.params.get('category.transition_in','Random')
            active.transition_out = self.request.params.get('category.transition_out','Random')
            active.d2l_folder = self.request.params.get('category.d2l_folder','')
            
            assesment_data = []
            for key,v in self.request.params.iteritems():
                if Validate.sanatize(v) != '':
                    if key.startswith('assessment'):
                        field_data = key.split('.')
                        row = {}
                        if not any(a['id'] == field_data[-1] for a in assesment_data):
                            assesment_data.append(row)
                        else:
                            row = filter(lambda x: x['id'] == field_data[-1], assesment_data)[0]
                        row['id'] = field_data[-1]
                        if v.isdigit():
                            row[field_data[1]] = int(v)
                        else:  
                            row[field_data[1]] = v
            active.set_assessments(assesment_data)
            
            editors = []
            if  self.request.params.getall('category.editable'):
                editors = self.request.params.getall('category.editable')
            else:
                for g in active.groups:
                    if g.edit:
                        editors.append(str(g.groups_id))
                        
            reviewers = []
            if  self.request.params.getall('category.reviewable'):
                reviewers = self.request.params.getall('category.reviewable')
            else:
                for g in active.groups:
                    if g.edit:
                        editors.append(str(g.groups_id))
            
            active.set_groups(self.request.params.getall('category.playable'), editors, reviewers)
            DBSession.flush()
            transaction.commit()
            if 'form.submit.questions' in self.request.params:
                return HTTPFound(location=self.request.application_url + '/edit/category/' + category_id + '/questions')
            return HTTPFound(location=self.request.application_url + '/edit/category/' + category_id)
        elif category_id == 'add':
            self.response['active_category'] = Categories(name='New Category')
        else:
            self.response['active_category'] = Categories.by(category_id, sort='position asc', user=self.request.user, permission=ACL.EDIT, strict=True).first()

        self.response['transitions_in'] = self.response['active_category'].transition_in
        self.response['transitions_out'] = self.response['active_category'].transition_out
        self.response['transitions'] = Transitions.all()
        
        self.response['all_edit_groups'] = Groups.by({'edit':True}).all()
        self.response['all_play_groups'] = Groups.by({'play':True}).all()
        self.response['all_review_groups'] = Groups.by({'review':True}).all()
        self.response['play_groups'] =  []
        self.response['edit_groups'] =  []
        self.response['review_groups'] =  []
        
        if self.response['active_category'].groups:
            for categorygroup in self.response['active_category'].groups:
                group = Groups.by(categorygroup.groups_id).first()
                if categorygroup.edit:
                    self.response['edit_groups'].append(group.name) 
                if categorygroup.play:
                    self.response['play_groups'].append(group.name) 
                if categorygroup.review:
                    self.response['review_groups'].append(group.name) 
            
        return self.template('/edit-category.pt', theme='AdminPanel')

        
        
        
        
        
        
        
        
        
        
        
        