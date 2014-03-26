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
from quizsmith.app.utilities import ACL
from quizsmith.admin import EditBaseView

import transaction

class EditView(EditBaseView):

    @view_config(route_name='edit_home', permission=ACL.EDIT)
    def edit_home(self):
        if 'form.submit' in self.request.params:
            for k,v in self.request.params.iteritems():
                if k.isdigit():
                    c = Categories.by(k).first()
                    c.position = v;
                    DBSession.flush()
            transaction.commit()
            return HTTPFound(location=self.request.application_url + '/edit')
        return self.template('/edit-home.pt', theme='AdminPanel')
        
        

        
        
        
        
        
        
        
        
        
        
        