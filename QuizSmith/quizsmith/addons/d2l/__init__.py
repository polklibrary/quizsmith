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

from quizsmith.app.utilities import add_route
from quizsmith.setup import Addons
from quizsmith.app.utilities.utility import Validate

def addon(config):

    if Validate.bool(config.registry.settings.get('d2l_on','False')) == False:
        return config
    
    # D2L Routes
    add_route(config, 'd2l_authorization', '/d2l/login')
    add_route(config, 'd2l_dropbox_submit', '/d2l/dropbox/submit')
    add_route(config, 'd2l_dropbox', '/d2l/dropbox/{id}')
    add_route(config, 'd2l_instructor_grades', '/d2l/instructors/grades/{id}')
    
    Addons.register('D2L Integration','1.0.0')
    config.scan()
    return config
    
    
    