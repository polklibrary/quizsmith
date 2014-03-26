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

from pyramid.httpexceptions import HTTPFound, HTTPForbidden
from pyramid.security import remember
from pyramid.url import route_url
from pyramid.view import view_config
from pyramid_mailer import get_mailer
from pyramid_mailer.message import Attachment,Message

from quizsmith.app.views import BaseView
from quizsmith.app.views.authentication import Authentication
from quizsmith.app.views.score import Score
from quizsmith.app.models import Users, Groups, Categories, Tests
from quizsmith.app.utilities import ACL,Validate

import d2lvalence.auth as d2lauth
import d2lvalence.data as d2ldata
import d2lvalence.service as d2lservice
import json
import requests
import traceback
import urllib
import StringIO


# D2L Login Hook
def d2l_login_layer(self):
    if Validate.bool(self.settings('d2l_on','false')) and not Validate.bool(self.request.params.get('local','0')):
        self.response['category'] = self.request.params.get('category','')
        return self.template('login.pt', theme='D2L')
    return None
Authentication.register_login_layer(d2l_login_layer)
        
        
ac = None # I don't like this but it is how D2L says to do it

class D2L(BaseView):
 
    def get_user_context(self):
        try:
            if not self.check_tokens():
                return HTTPFound(location=self.get_app_context().create_url_for_authentication(self.settings('d2l_domain'), self.request.url))
            return self.get_app_context().create_user_context(result_uri=self.request.url, host=self.settings('d2l_domain'), encrypt_requests=True)
        except Exception as e:
            return HTTPForbidden()

    def get_app_context(self):
        global ac
        if ac == None:
            app_creds = { 'app_id': self.settings('d2l_app_id'), 'app_key': self.settings('d2l_app_key') }
            ac = d2lauth.fashion_app_context(app_id=app_creds['app_id'], app_key=app_creds['app_key'])
        return ac
        
    def check_tokens(self):
        return ('x_a' in self.request.params and 'x_b' in self.request.params and 'x_c' in self.request.params)
 
 
class D2LLogin(D2L):
        
    @view_config(route_name='d2l_authorization')
    def d2l_authorization(self):
        uc = self.get_user_context()
        if not isinstance(uc, d2lauth.D2LUserContext):
            return uc # if no user_context is setup, return uc to d2l to get authorized.
        
        try:
            whoami = d2lservice.get_whoami(uc)
            id = str(whoami.UniqueName) + self.settings('d2l_append_email_address','')
            fullname = whoami.FirstName + u' ' + whoami.LastName
            
            # if doesn't exist create it and update login info
            category = self.request.params.get('category','0')
            user = Users.by({'email':id}).first()
            if not user:
                Users.registerNonLocalUser(email=id, fullname=fullname)
                user = Users.by({'email':id}).first() #retrieve new user
            
            # auto group incoming users
            if Validate.bool(self.request.params.get('group','false')):
                user = Users.add_groups(user, Groups.groups_auto_assigned_by_category(category))
            
            user = Users.login_updates(user)
            
            # set session and send them to alias controller
            return HTTPFound(location=route_url('alias', self.request, _query={'category':category} ), 
                             headers=remember(self.request, user.id))

        except Exception as e:
            print "ERROR 0: " + str(e) # log later?
        return HTTPForbidden() 
        


class D2LDropBox(D2L):

    def set_default_responses(self):
        self.response['id'] = 0
        self.response['status'] = 0
        self.response['courses'] = []
        
        
    @view_config(route_name='d2l_dropbox', permission=ACL.AUTHENTICATED)
    def d2l_dropbox(self):
        self.set_default_responses()
        uc = self.get_user_context()
        if not isinstance(uc, d2lauth.D2LUserContext):
            return uc # if no user_context is setup, return uc to d2l to get authorized.
            
        try:
            id = self.request.matchdict['id']
            courses = d2lservice.get_my_enrollments(uc)
            for course in courses.Items:
                try:
                    folders = d2lservice.get_all_dropbox_folders_for_orgunit(uc, course['OrgUnit']['Id'])
                    folder_id = self.check_for_d2l_folder(id, folders)
                    if folder_id:
                        self.response['courses'].append({'org_unit':course['OrgUnit']['Id'],
                                                         'name':course['OrgUnit']['Name'],
                                                         'folder_id':folder_id,
                                                        })
                except Exception as e:
                    pass # This exception is to catch any unwanted 403's from D2L and not throw an error
            
            self.response['id'] = id
            return self.template('dropbox.pt', theme='D2L') 
            
        except Exception as e:
            print "ERROR 1: " + str(e)
        return HTTPForbidden()
        
        
    @view_config(route_name='d2l_dropbox_submit', permission=ACL.AUTHENTICATED)
    def d2l_dropbox_submit(self):
        self.set_default_responses()
        uc = self.get_user_context()
        if not isinstance(uc, d2lauth.D2LUserContext):
            return uc # if no user_context is setup, return uc to d2l to get authorized.
        
        try:
            test_id = self.request.params.get('id','0')
            course = self.request.params.get('course_info','0|0').split('|')
            course_org_unit = course[0]
            d2l_folder = course[1]
            pdf = Score(self.request)._generate_pdf(test_id)
            test = Tests.by(test_id).first()
            submission = d2ldata.D2LDropboxSubmission({'Name':'ANVIL_Submission_ID-' + test_id + '.pdf',
                                                       'DescriptorDict':{'Text': None, 'HTML':None}, 
                                                       'Stream':StringIO.StringIO(pdf), 
                                                       'ContentType':'application/pdf',
                                                      })
            response = d2lservice.create_my_submission_for_dropbox(uc, course_org_unit, d2l_folder, submission, return_request=True)
            self.response['id'] = test_id
            self.response['status'] = response.status_code
            self.response['category'] = test.category
            return self.template('dropbox.pt', theme='D2L')
            
        except Exception as e:
            print "ERROR 2: " + str(e) # log later?
        return HTTPForbidden()
        
        
    def check_for_d2l_folder(self, id, folders):
        test = Tests.by(id).first()
        for folder in folders:
            if folder['Name'] == test.d2l_folder:
                return folder['Id']
        return None
        