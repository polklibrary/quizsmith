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
from quizsmith.app.models import DBSession,Groups,Users,Categories
from quizsmith.app.utilities import ACL,Validate
from quizsmith.admin import EditBaseView

import transaction

class EditView(EditBaseView):

    @view_config(route_name='edit_groups', permission=ACL.ADMIN)
    def edit_groups(self):
        lookup = self.request.params.get('edit.user.find','')
        self.response['email'] = self.request.params.get('edit.user.find.email','')
        self.response['user'] = Users.by({'email':self.response['email']}).first()
        if self.response['user'] and lookup:
            self.notify('User found')
        if self.response['email'] and not self.response['user'] and lookup:
            self.notify('No user found',warn=True)
        self.response['editing_group'] = None

        # add/remove users from groups
        if 'edit.user.group.add.submit' in self.request.params:
            id = self.request.params.get('edit.user.group.add','')
            group = Groups.by(id).first()
            self.response['user'].groups.append(Groups.by(id).first())
            transaction.commit()
            self.notify('Added user to group')
            self.response['editing_group'] = Groups.by(id).first()
            self.response['user'] = Users.by({'email':self.response['email']}).first()
            
        if 'edit.user.group.remove.submit' in self.request.params:
            id = self.request.params.get('edit.user.group.remove','')
            self.response['user'].groups.remove(Groups.by(id).first())
            transaction.commit()
            self.notify('Removed user from group')
            self.response['user'] = Users.by({'email':self.response['email']}).first()
            
        if 'edit.group.find.submit' in self.request.params:
            id = self.request.params.get('edit.group.find','')
            self.response['editing_group'] = Groups.by(id).first()
            
        if 'edit.group.edit.submit' in self.request.params:
            id = self.request.params.get('edit.group.edit.id','')
            group = Groups.by(id).first()
            group.name = self.request.params.get('edit.group.edit.name','No name')
            group.description = self.request.params.get('edit.group.edit.description','No Description')
            group.play = Validate.bool(self.request.params.get('edit.group.edit.play', False))
            group.edit = Validate.bool(self.request.params.get('edit.group.edit.edit', False))
            group.review = Validate.bool(self.request.params.get('edit.group.edit.review', False))
            cats = []
            for cid in self.request.params.getall('edit.group.edit.categories'):
                cats.append(Categories.by(int(cid)).first())
            group.categories = cats
            
            transaction.commit()
            self.response['editing_group'] = Groups.by(id).first()
            self.notify('Changes saved!')
            
        if 'edit.group.new.submit' in self.request.params:
            i = Groups.newest().id + 1
            DBSession.add(Groups(name='New Group' + str(i)))
            transaction.commit()
            self.response['editing_group'] = Groups.newest()
            self.notify('Added group!')
            
        if 'edit.group.delete.submit' in self.request.params:
            id = int(self.request.params.get('edit.group.find','0'))
            if id not in [1,2,3]:
                try:
                    group = Groups.by(id).first()
                    DBSession.delete(group)
                    transaction.commit()
                    self.notify('Removed group!')
                except exc.SQLAlchemyError:
                    self.notify("You can't delete this group.  It has user and category dependencies.",warn=True)
            else:
                self.notify("Can't remove permanent group!",warn=True)
            
        self.response['groups'] = Groups.all()
        self.response['categories'] = Categories.all()
        
        return self.template('/edit-groups.pt', theme='AdminPanel')
