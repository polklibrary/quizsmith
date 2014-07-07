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
from quizsmith.admin import EditBaseView
from quizsmith.app.models import DBSession
from quizsmith.app.utilities import ACL
from quizsmith.setup import Import

import transaction

class EditView(EditBaseView):

    @view_config(route_name='edit_delete', permission=ACL.EDIT)
    def edit_delete(self):
        id = self.request.matchdict['id']
        classname = str(self.request.matchdict['type'])
        back = self.request.params.get('back',None)
        if back == None or not back.startswith(self.request.application_url):
            return HTTPFound(location=self.request.application_url) 
        
        type = Import('quizsmith.app.models',str(classname))
        obj = DBSession.query(type).filter(type.id==id).first()
        if obj:
            DBSession.delete(obj)
            DBSession.flush()
        
        transaction.commit() # make it so number one
        self.notify('Removed!')
        return HTTPFound(location=self.request.params['back'])
