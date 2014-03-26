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

from pyramid.view import view_config
from quizsmith.app.models import Properties
from quizsmith.app.utilities import ACL
from quizsmith.admin import EditBaseView

import transaction

class EditView(EditBaseView):

    @view_config(route_name='edit_mailer', permission=ACL.ADMIN)
    def edit_mailer(self):
    
        if 'edit.mailer.submit' in self.request.params:
            msubject = Properties.by({'prop_name':'MAILER_TO_SUBJECT'}).first()
            msubject.prop_value = self.request.params.get('edit.mailer.subject','')
            mfrom = Properties.by({'prop_name':'MAILER_GLOBAL_FROM_ADDRESS'}).first()
            mfrom.prop_value = self.request.params.get('edit.mailer.from','')
            mfeedback = Properties.by({'prop_name':'MAILER_FEEDBACK_ADDRESS'}).first()
            mfeedback.prop_value = self.request.params.get('edit.mailer.feedback','')
            mbody = Properties.by({'prop_name':'MAILER_BODY'}).first()
            mbody.prop_value = self.request.params.get('edit.mailer.body','')
            transaction.commit()
            self.response['message'] = "Mailer Settings Changed"
            self.response['message_class'] = "info"
            
        self.response['mailer'] = {'subject': Properties.get('MAILER_TO_SUBJECT',''),
                                   'from_address': Properties.get('MAILER_GLOBAL_FROM_ADDRESS',''),
                                   'feedback_address': Properties.get('MAILER_FEEDBACK_ADDRESS',''),
                                   'body': Properties.get('MAILER_BODY',''),
                                   }

        return self.template('/edit-mailer.pt', theme='AdminPanel')  
