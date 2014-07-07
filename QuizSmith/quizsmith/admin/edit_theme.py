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

from pyramid.httpexceptions import HTTPFound, HTTPForbidden
from pyramid.response import Response
from pyramid.view import view_config
from quizsmith.app.models import Properties
from quizsmith.app.utilities import ACL
from quizsmith.admin import EditBaseView

import transaction,zipfile,shutil,StringIO,pkg_resources,os,ConfigParser,datetime

class EditView(EditBaseView):
        
    @view_config(route_name='edit_theme', permission=ACL.ADMIN)
    def edit_theme(self):
        self.determine_instance('AdminPanel') # since instance_id is needed earlier than render time, determine it by calling sooner.
        self.response['changeable_themes'] = []
        self.response['deletable_themes'] = []
        self.response['all_themes'] = []
        
        try:
            if 'edit.theme.change.submit' in self.request.params:
                theme_name = self.request.params.get('edit.theme.change','**SimpleBlue')
                theme_name = theme_name.replace('**','')
                p = Properties.by({'prop_name':'ACTIVE_THEME'}).first()
                p.prop_value = theme_name
                transaction.commit()
                self.notify('Theme changed to ' + theme_name + '!')
                return HTTPFound(location=self.request.application_url + '/edit/theme')
                
            if 'edit.theme.upload.submit' in self.request.params:
                theme_dir = pkg_resources.resource_filename('quizsmith', 'themes/' + self.settings('theme.folder'))
                os.chdir(theme_dir)
                obj = self.request.params.get('edit.theme.upload','')
                zip = zipfile.ZipFile(obj.file, 'r')
                filename = os.path.splitext(os.path.basename(obj.filename))[0]
                allowed_extensions = tuple(self.settings('safe_uploads_ext','').split(','))
                
                try:
                    shutil.rmtree(filename)
                except Exception as e:
                    pass # ignore if folder didn't previously exist
                
                if not self.has_python(zip):
                    firstpass = True
                    for f in zip.namelist():
                        if firstpass and not f.endswith('/'): # created folder if not nested zip
                            os.makedirs(filename)
                            os.chdir(filename)
                        if f.endswith('/'):
                            os.makedirs(f)
                        elif f.endswith(allowed_extensions):
                            zip.extract(f)
                        firstpass = False
                    self.notify('Theme Uploaded: ' + str(filename))
                
            if 'edit.theme.remove.submit' in self.request.params:
                value = self.request.params.get('edit.theme.remove','')
                shutil.rmtree(value)
                self.notify('Theme Removed!  This cannot be undone.')
                
        except Exception as e:
            print str(e)
            self.notify('Could not complete',warn=True)
            
        self.load_themes('default','**')
        self.load_themes(self.settings('theme.folder'),'')
        return self.template('/edit-theme.pt', theme='AdminPanel')

        
    def load_themes(self,instance,prefix):
        theme_dir = pkg_resources.resource_filename('quizsmith', 'themes/' + instance)
        os.chdir(theme_dir)
        folders = [d for d in os.listdir('.') if os.path.isdir(d)]
        for f in folders:
            for s in os.listdir(f):
                if s == 'theme.ini':
                    config_file = os.path.abspath(os.path.join(f, s))
                    config = ConfigParser.ConfigParser()
                    config.read(config_file)
                    if config.getboolean('Theme', 'theme.can_be_activated'):
                        self.response['changeable_themes'].append( prefix + str(f) )
                    if config.getboolean('Theme', 'theme.can_be_delete'):
                        self.response['deletable_themes'].append( prefix + str(f) )
                    self.response['all_themes'].append( prefix + str(f) )
        
       
    @view_config(route_name='export_theme', permission=ACL.EDIT)
    def export_theme(self):
        theme_name = self.request.matchdict['theme_name']
        instance = 'default'
        if '**' not in theme_name.lower():
            instance = self.settings('theme.folder')
        
        theme_name = theme_name.replace('**','')
        theme_file = '[Theme]' + '\n' +\
                     'theme.can_be_delete=True' + '\n' +\
                     'theme.can_be_activated=True' + '\n' +\
                     'theme.quizsmith.version=' + str(self.settings('version'))
        
        path = pkg_resources.resource_filename('quizsmith', 'themes/' + instance)
        os.chdir(path)
        
        io = StringIO.StringIO()
        zip = zipfile.ZipFile(io, 'w', compression=zipfile.ZIP_DEFLATED)
        root_len = len(os.path.abspath(theme_name))
        
        for root, dirs, files in os.walk(theme_name):
            archive_root = os.path.abspath(root)[root_len:]
            for f in files:
                fullpath = os.path.join(root, f)
                archive_name = os.path.join(archive_root, f)
                if f == 'theme.ini':
                    zip.writestr(archive_name, theme_file, zipfile.ZIP_DEFLATED)
                else:
                    zip.write(fullpath, archive_name, zipfile.ZIP_DEFLATED)
        zip.close()
        io.seek(0)
        file = io.read()
        io.close()
        return Response(content_type='application/zip', content_disposition='attachment; filename="' + theme_name + '.zip"', body=file)

        
    def has_python(self,zip):
        """ Simple scan of files for key words """
        for f in zip.namelist():
            print 'f: ' + str(f)
            if not f.endswith(('.png','.gif','.jpg','.jpeg','.tif','.tiff','.bmp')):
                if f.endswith('.pt'):
                    content = zip.read(f)
                    if '<?' in content or '?>' in content or 'python:' in content:
                        self.notify('Failed: Python detected in ' + str(f), warn=True)
                        return True
        return False
        
        
        
        
        
        
        
        
        
        
        
        