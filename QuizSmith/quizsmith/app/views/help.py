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
from quizsmith.app.views import BaseView
from pyramid_mailer import get_mailer
from pyramid_mailer.message import Attachment,Message
from quizsmith.app.utilities import ACL,Validate
from quizsmith.app.models import Properties

import datetime

class Help(BaseView):

    @view_config(route_name='help')
    def help(self):
        self.response['help_address'] = Properties.get('MAILER_HELP_ADDRESS',default='')
        return self.template('help.pt')
        
        
    @view_config(route_name='feedback', renderer='json', permission=ACL.AUTHENTICATED)
    def feedback(self):
        self.response['sent_status'] = 0
        if 'feedback.message' in self.request.params:
            msg = Validate.sanatize_textsafe(self.request.params.get('feedback.message',''))
            msg = msg + "\n\n ---------- \n"
            msg = msg + "Player: " + self.request.params.get('feedback.player','error') + "\n"
            msg = msg + "Category: " + self.request.params.get('feedback.category','error') + "\n"
            msg = msg + "From: " + self.request.params.get('feedback.from','error') + "\n"
            
            try:
                # Send to 
                emails = Properties.get('MAILER_FEEDBACK_ADDRESS').replace(' ','').split(',')
                message = Message(subject="Feedback - " + datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
                                  sender=self.request.user.email,
                                  recipients=emails,
                                  body=msg
                                  )
                mailer = get_mailer(self.request)
                mailer.send(message)
                
                # Receipt
                message_receipt = Message(subject="Feedback - Receipt",
                                  sender=Properties.get('MAILER_GLOBAL_FROM_ADDRESS'),
                                  recipients=[self.request.user.email],
                                  body="Thank you for submitting feedback. \n\n ---- \n" + Validate.sanatize_textsafe(self.request.params.get('feedback.message',''))
                                  )
                mailer.send(message_receipt)
                
                self.response['sent_status'] = 2
            except Exception as e:
                self.response['sent_status'] = 1
        return self.response