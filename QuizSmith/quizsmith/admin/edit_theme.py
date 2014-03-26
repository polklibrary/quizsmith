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

import transaction,zipfile,shutil,StringIO,pkg_resources,os

class EditView(EditBaseView):
        
    @view_config(route_name='edit_theme', permission=ACL.ADMIN)
    def edit_theme(self):
        theme_dir = pkg_resources.resource_filename('quizsmith', 'themes/')
        os.chdir(theme_dir)
        
        try:
            if 'edit.theme.change.submit' in self.request.params:
                value = self.request.params.get('edit.theme.change','')
                p = Properties.by({'prop_name':'ACTIVE_THEME'}).first()
                p.prop_value = value
                transaction.commit()
                self.response['message'] = 'Theme Changed'
                self.response['message_class'] = 'info'
                
            if 'edit.theme.upload.submit' in self.request.params:
                obj = self.request.params.get('edit.theme.upload','')
                zip = zipfile.ZipFile(obj.file, 'r')
                filename = os.path.splitext(os.path.basename(obj.filename))[0]
                allowed_extensions = tuple(self.settings('safe_uploads_ext','').split(','))
                
                try:
                    shutil.rmtree(filename)
                except Exception as e:
                    pass # ignore if folder didn't previously exist
                
                os.makedirs(filename)
                os.chdir(filename)
                for f in zip.namelist():
                    if f.endswith('/'):
                        os.makedirs(f)
                    elif f.endswith(allowed_extensions):
                        zip.extract(f)
                self.response['message'] = 'Theme Uploaded'
                self.response['message_class'] = 'info'
                os.chdir(theme_dir)
                
            if 'edit.theme.remove.submit' in self.request.params:
                value = self.request.params.get('edit.theme.remove','')
                shutil.rmtree(value)
                self.response['message'] = 'Theme Removed'
                self.response['message_class'] = 'info'
                
        except Exception as e:
            self.response['message_class'] = "warn"
            if self.response['message'] == '':
                self.response['message'] = 'Could not complete'
            print str(e)
            
        folders = [d for d in os.listdir('.') if os.path.isdir(d)]
        self.response['restricted_themes'] = []
        self.response['all_themes'] = []
        for f in folders:
            if not any('EXCLUDE_THEME' in s for s in os.listdir(f)):
                self.response['restricted_themes'].append( str(f) )
            self.response['all_themes'].append( str(f) )
            
        return self.template('/edit-theme.pt', theme='AdminPanel')

        
    @view_config(route_name='export_theme', permission=ACL.EDIT)
    def export_theme(self):
        path = pkg_resources.resource_filename('quizsmith', 'themes/')
        os.chdir(path)
        dir = self.request.matchdict['theme_name']

        io = StringIO.StringIO()
        zip = zipfile.ZipFile(io, 'w', compression=zipfile.ZIP_DEFLATED)
        root_len = len(os.path.abspath(dir))
        
        for root, dirs, files in os.walk(dir):
            archive_root = os.path.abspath(root)[root_len:]
            for f in files:
                fullpath = os.path.join(root, f)
                archive_name = os.path.join(archive_root, f)
                zip.write(fullpath, archive_name, zipfile.ZIP_DEFLATED)
        zip.close()
        io.seek(0)
        file = io.read()
        io.close()
        return Response(content_type='application/zip', body=file)


    def zipper(self, dir):
        io = StringIO.StringIO()
        zip = zipfile.ZipFile(io, 'w', compression=zipfile.ZIP_DEFLATED)
        root_len = len(os.path.abspath(dir))
        for root, dirs, files in os.walk(dir):
            archive_root = os.path.abspath(root)[root_len:]
            for f in files:
                fullpath = os.path.join(root, f)
                archive_name = os.path.join(archive_root, f)
                zip.write(fullpath, archive_name, zipfile.ZIP_DEFLATED)
        zip.close()
        io.seek(0)
        file = io.read()
        io.close()
        return file
        