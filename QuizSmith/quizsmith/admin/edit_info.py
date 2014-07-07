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
from quizsmith.app.models import Users,Properties
from quizsmith.app.utilities import ACL
from quizsmith.admin import EditBaseView

import transaction

class EditView(EditBaseView):

    @view_config(route_name='edit_info', permission=ACL.EDIT)
    def edit_info(self):
    
        # Analytics
        if 'edit.info.analytics.submit' in self.request.params:
            value = self.request.params.get('edit.info.analytics','')
            analytics = Properties.by({'prop_name':'ANALYTICS'}).first()
            analytics.prop_value = value
            transaction.commit()
            self.notify('Changes saved!')
        self.response['analytics'] = Properties.get('ANALYTICS',default='')
        
        # Site User Information
        users = Users.by(None,sort='last_active desc')
        self.response['users_last_active'] = users.all()[0:5]
        self.response['users_local_count'] = users.filter(getattr(Users,'is_local')==True).count()
        self.response['users_non_local_count'] = users.filter(getattr(Users,'is_local')==False).count()
        self.response['users_total_count'] = users.count()
        return self.template('/edit-info.pt', theme='AdminPanel')
