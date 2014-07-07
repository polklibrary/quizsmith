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

from operator import itemgetter
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from quizsmith.app.models import DBSession,Properties
from quizsmith.app.utilities import ACL
from quizsmith.admin import EditBaseView

import transaction,json,collections

class EditView(EditBaseView):

    @view_config(route_name='edit_credits', permission=ACL.EDIT)
    def edit_credits(self):
    
        if 'edit.credits.submit' in self.request.params:
            i = 0
            results = []
            for k in self.request.params:
            
                if 'data_' in k:
                    p = k.split('_')
                    d = { 'id':int(p[1]) }
                    exists = False
                    for r in results:
                        if r['id'] == int(p[1]):
                            d = r
                            exists = True
                    if '_type' in k:
                        d['type'] = self.request.params.get(k)
                    if '_val' in k:
                        d['value'] = self.request.params.get(k)
                    if not exists:
                        results.append(d)
                       
            results = sorted(results,key=itemgetter('id'))
            properties = Properties.by({'prop_name':'CREDITS'}).first()
            properties.prop_value = json.dumps(results)
            transaction.commit()
            self.notify('Changes saved!')
            
        self.response['credits'] = json.loads(Properties.get('CREDITS','[]'))
        
        return self.template('/edit-credits.pt', theme='AdminPanel')
