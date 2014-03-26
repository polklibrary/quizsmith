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
from pyramid.url import route_url
from quizsmith.app.views import BaseView
from quizsmith.app.utilities import ACL
from quizsmith.app.models import Categories,Users


class Category(BaseView):

    @view_config(route_name='category', permission=ACL.AUTHENTICATED)
    def category(self):
        if not self.request.user.alias:
            return HTTPFound(location=route_url('alias', self.request))
        self.response['categories'] = Categories.by(None, sort='position asc', user=self.request.user, permission=ACL.PLAY)
        return self.template('category.pt')
        
        
    @view_config(route_name='category_intro', permission=ACL.AUTHENTICATED)
    def category_intro(self):
        category = int(self.request.matchdict['id'])
        
        if category:
            self.response['category'] = Categories.by(category, user=self.request.user, permission=ACL.PLAY).first()
            return self.template('category_intro.pt')
            
        return HTTPFound(location=route_url('category', self.request))