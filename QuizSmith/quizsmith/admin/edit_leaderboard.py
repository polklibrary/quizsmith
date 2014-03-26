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

from pyramid.response import Response
from pyramid.view import view_config
from quizsmith.app.models import Properties
from quizsmith.app.utilities import ACL
from quizsmith.admin import EditBaseView

import transaction

class EditView(EditBaseView):

    @view_config(route_name='edit_leaderboard', permission=ACL.EDIT)
    def edit_leaderboard(self):
        
        if 'edit.leaderboard.submit' in self.request.params:
            archive_date = Properties.by({'prop_name':'LEADERBOARD_ARCHIVE_DATE'}).first()
            archive_date.prop_value = self.request.params.get('edit.leaderboard.archive_date','2013-1-1')
            transaction.commit()
            self.response['message'] = "Leaderboard Settings Changed"
            self.response['message_class'] = "info"
        
        self.response['leaderboard'] = {'archive_date': Properties.get('LEADERBOARD_ARCHIVE_DATE','2013-1-1'),
                                        }
        
        return self.template('/edit-leaderboard.pt', theme='AdminPanel')

