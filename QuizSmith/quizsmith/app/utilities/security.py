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

from pyramid_formalchemy.resources import Models
from pyramid.decorator import reify
from pyramid.request import Request
from pyramid.security import Allow, Authenticated, ALL_PERMISSIONS, Everyone, unauthenticated_userid, has_permission
from quizsmith.app.models import DBSession, Users, Groups, Properties

import datetime
import transaction

def groupfinder(userid, request):
    if Users.by(userid).first():
        results = DBSession.query(Users,Groups).filter(Users.id == userid).join(Users.groups).all()
        return [result.Groups.name for result in results]
    return []

class ACL(object):

    ANONYMOUS = "Anonymous"
    AUTHENTICATED = "Authenticated"
    PLAY = "Play"
    EDIT = "Edit"
    REVIEW = "Review"
    ADMIN = "Administrate"

    @classmethod
    def factory(cls):
        aclist = [(Allow,Everyone,cls.ANONYMOUS),(Allow,Authenticated,cls.AUTHENTICATED),]   
        for group in DBSession.query(Groups).all():
            aclist.append((Allow, group.name, group.permissions()))
        return aclist
    
    @classmethod
    def enforce_rights(cls,acl):
        for i,a in enumerate(acl):
            if ACL.ADMIN in a[-1]:
                acl[i] = (a[0],a[1],ALL_PERMISSIONS)
        return acl
    
    
class RootACL(object):
    """ Root ACL for site root, permissions are inherited downwards """

    __name__ = None
    __parent__ = None

    def __init__(self, request):
        self.request = request

    def has_permissions(self, permissions):
        """ String or List Allowed """ 
        if isinstance(permissions, list):
            for permission in permissions:
                if has_permission(permission, self, self.request):
                    return True
            return False
        else:
            return has_permission(permissions, self, self.request)
        
    @property
    def __acl__(self):
        return ACL.enforce_rights(ACL.factory())
        
        
class PyramidFormalchemyACL(Models):
    """ Root ACL for Pyramid FormAlchemy """
    
    @property
    def __acl__(self):
        acl = ACL.factory()
        acl = filter(lambda x: ACL.ADMIN in x[-1] or ACL.EDIT in x[-1], acl)
        return ACL.enforce_rights(acl)
        
        
class RequestExtension(Request):
    """ Extend request object and add in useful data """

    errors = ''
    
    @property
    def notification(self):
        msg = self.session.pop_flash()
        if msg:
            return msg[0]
        return None
       
    @property
    def user(self):
        userid = unauthenticated_userid(self)
        if userid is not None:
            return Users.by(userid).first()
    
    @reify
    def day_caching(self):
        return '?day-cache=' + datetime.datetime.today().strftime('%Y%m%d')
        
    @reify
    def no_caching(self):
        return '?no-cache=' + str(datetime.datetime.now())
    
    @reify
    def application_url(self):
        return super(RequestExtension, self).application_url + self.registry.settings.get('virtual_path_ext','')
    
    @reify
    def active_base_theme(self):
        return Properties.get('ACTIVE_THEME','Original')

    @property
    def can_edit(self):
        return self.has_permissions(['Edit','Administrate'])
        
    @property  
    def can_admin(self):
        return self.has_permissions(['Administrate'])
        
    def has_permissions(self,permissions):
        """ String or List Allowed """ 
        if isinstance(permissions, list):
            for permission in permissions:
                if has_permission(permission, self.context, self):
                    return True
            return False
        else:
            return has_permission(permissions,self.context,self)
