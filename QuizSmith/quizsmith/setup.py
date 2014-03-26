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

import pkgutil, traceback

def Import(module_name,class_name):
    """ Dynamic Import to protect against Circular Import Errors """
    mod = __import__(module_name, fromlist=[class_name])
    return getattr(mod, class_name)
    
class Addons(object):

    registered = []
    
    @classmethod
    def get_version(cls,name):
        for package in cls.registered:
            if package[0] == name:
                return package[1]
        return '0.0.0'

    @classmethod
    def load_addons(cls,config,level):
        """ Locates and loads modules inside QuizSmith """
        for importer, modname, ispkg in pkgutil.iter_modules(level.__path__):
            try:    
                if ispkg:
                    pkg = Import(level.__name__, modname)
                    if hasattr(pkg, 'addon'):
                        config = pkg.addon(config)
            except Exception as e:
                print "ERROR! " + modname + " FAILED TO IMPORT CORRECTLY"
                traceback.print_exc()
     
        return config
    
    @classmethod
    def register(self,name,version):
        self.registered.append((name,version))
    