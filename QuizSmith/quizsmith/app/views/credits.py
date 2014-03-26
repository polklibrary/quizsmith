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
from pyramid.url import route_url
from pyramid.view import view_config

from quizsmith.app.models import Users
from quizsmith.app.views import BaseView
from quizsmith.app.utilities import ACL,Validate

import transaction

class Credits(BaseView):

    @view_config(route_name='credits')
    def credits(self):
        
        return self.template('credits.pt')
        
