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

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from quizsmith.setup import Import,Addons
from quizsmith.app.models import DBSession
from quizsmith.app.utilities import groupfinder, RootACL, RequestExtension

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application. """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    authorization_policy = ACLAuthorizationPolicy()
    authentication_policy = AuthTktAuthenticationPolicy('auth.secret', callback=groupfinder)
    
    config = Configurator(settings=settings,
                          authentication_policy=authentication_policy,
                          authorization_policy=authorization_policy,
                          request_factory=RequestExtension,
                          root_factory=RootACL)
    
    config.add_static_view('themes', 'quizsmith:themes')
    
    import quizsmith
    config = Addons.load_addons(config,quizsmith)

    try:
        config = Addons.load_addons(config,quizsmith.addons)
    except:
        print "Could not find addons directory"
            
    print "\n-- Modules ---------------------- "
    for addon in Addons.registered:
        print addon[0] + ' == ' + addon[1]
    print "-- Modules ---------------------- \n"
    
    return config.make_wsgi_app()

    