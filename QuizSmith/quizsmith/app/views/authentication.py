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

from pyramid.httpexceptions import HTTPFound,HTTPForbidden,HTTPNotFound
from pyramid.security import remember,forget
from pyramid.url import route_url
from pyramid.view import view_config,forbidden_view_config
from quizsmith.app.models import Users,DBSession
from quizsmith.app.views import BaseView
from quizsmith.app.utilities import ACL,Validate
import transaction, datetime, types

        
class Authentication(BaseView):

    login_layers = []

    @classmethod
    def register_login_layer(cls, fn):
        cls.login_layers.insert(0,fn)
        
    @view_config(route_name='login')
    def login(self):
        self.response['allow_registration'] = Validate.bool(self.settings('allow_local_registration','false'))
        if self.request.user:
            return HTTPFound(location=route_url('alias', self.request, _query={'category':self.request.params.get('category',0)}))
            
        for fn in self.login_layers:
            layer = fn(self)
            if layer:
                return layer
        
    def local_login(self):
        if 'form.submitted' in self.request.params:
            user = Users.by({'is_local':True, 'email':self.request.params['email']}).first()
            if user and user.validate_password(self.request.params['password']):
                user = Users.login_updates(user);
                return HTTPFound(location=route_url('alias', self.request), headers=remember(self.request, user.id))
            self.response['message'] = 'Please check your username or password'
        return self.template('login.pt')

    @view_config(route_name='logout')
    def logout(self):
        if 'redirect' in self.request.params:
            headers = forget(self.request)
            return HTTPFound(location=self.request.params.get('redirect'), headers=headers)
        else:
            headers = forget(self.request)
            return HTTPFound(location=route_url('menu', self.request), headers=headers)
    
    @view_config(route_name='register',)
    def register(self):
        if not Validate.bool(self.settings('allow_local_registration','false')):
            return HTTPFound(location=route_url('menu', self.request))
    
        self.response['email'] = ''
    
        if 'form.submitted' in self.request.params:
            self.response['email'] = Validate.sanatize(self.request.params['email'])
            password = Validate.sanatize(self.request.params['password'])
            repassword = Validate.sanatize(self.request.params['re.password'])
            
            if Users.by({'email':self.response['email']}).first():
                self.response['message'] = "Email already in use"
                return self.template('register.pt')
            if not Validate.email(self.response['email']):
                self.response['message'] = "Not a valid email address"
                return self.template('register.pt')
            if not Validate.password(password):
                self.response['message'] = "Improper password."
                return self.template('register.pt')
            if repassword != password:
                self.response['message'] = "Passwords do not match."
                return self.template('register.pt')
                
            # Below is good
            Users.registerLocalUser(self.response['email'], password)
            return HTTPFound(location=route_url('login', self.request))
            
        return self.template('register.pt')

    @view_config(route_name='change_password', permission=ACL.AUTHENTICATED)
    def change_password(self):
        user = Users.by(self.request.user.id).first()
        if not user.is_local:
            return HTTPForbidden()

        if 'form.submitted' in self.request.params:
            old = Validate.sanatize(self.request.params['old_password'])
            new = Validate.sanatize(self.request.params['new_password'])
            recheck = Validate.sanatize(self.request.params['new_recheck_password'])
            
            if not Validate.password(new):
                self.response['message'] = "Improper new password."
                return self.template('change_password.pt')
            if recheck != new:
                self.response['message'] = "New passwords do not match."
                return self.template('change_password.pt')
            
            if user.validate_password(old):
                user._set_password(new)
                transaction.commit()
    
        return self.template('change_password.pt')
        
    @view_config(route_name='halt')
    def halt(self):
        return self.template('halt.pt',status=404)
    
    @view_config(context=HTTPForbidden)
    def unauthorized(self):
        self.response['message'] = "You do not have permissions to view this page. Please Login."
        return self.template('halt.pt',status=403)

    @view_config(context=HTTPNotFound)
    def not_found(self):
        self.request.response.status = 404
        self.response['message'] = "Page not found."
        return self.template('halt.pt',status=404)

        
Authentication.register_login_layer(Authentication.local_login)




    