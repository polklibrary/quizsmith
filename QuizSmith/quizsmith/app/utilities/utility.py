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
from email.utils import parseaddr
import re, datetime

class Validate(object):

    @classmethod
    def alias(cls,alias):
        """ TODO: improve later """
        return (len(alias) > 3 and len(alias) < 15 and re.match('^[A-Za-z0-9_-]+$', alias) is not None)

    @classmethod
    def password(cls,password):
        return (len(password) > 7 and len(password) < 20 and re.search('\d+',password) and re.search('[a-zA-Z]',password))

    @classmethod
    def email(cls,email):
        e = re.compile('([\w\-\.]+@(\w[\w\-]+\.)+[\w\-]+)')
        return (len(e.findall(email)) > 0)
        #return (parseaddr(email)[1] != '')

    @classmethod
    def sanatize_textsafe(cls,text):
        """ Remove all types of spaces """
        return re.sub('[<>/+{}&@~`]','',text)
        
    @classmethod
    def sanatize(cls,text):
        """ Remove all types of spaces """
        return text.replace(' ','')
        
    @classmethod
    def bool(cls,o):
        if isinstance(o, str) or isinstance(o, unicode):
            return o.lower() in ['true','t','y','yes','1','on']
        elif isinstance(o, int):
            return (o > 0)
        elif isinstance(o, list):
            return (len(o) > 0)
        else:
            return bool(o)

def empty(o,default):
    if o == '' or o == None or o == [] or o == {}:
        return default
    return o
    
def RemoveImages(data):
    p = re.compile(r'<img.*?/>')
    return p.sub('', data)
        
        
def Result2Dict(row,purge=[]):
    d = {}
    for column in row.__table__.columns:
        if column.name not in purge:
            if isinstance(getattr(row, column.name), datetime.datetime):
                d[column.name] = getattr(row, column.name).strftime('%m/%d/%Y %I:%M %p')
            else:
                d[column.name] = getattr(row, column.name)
    return d
    

def Seconds2Str(time):
    m,s = divmod(time, 60)
    if m == 0:
        return  "%s secs" % int(s)
    return "%d min %s secs" % (int(m), int(s))
    
    
def add_route(config, name, pattern, **kw):
    """ Adds trailing slash redirect """
    config.add_route(name, pattern, **kw)
    if not pattern.endswith('/'):
        config.add_route(name + '-auto', pattern + '/')
        def redirect(request):
            matchdict = request.matchdict.copy()
            url = request.route_url(name, traverse=(), **matchdict)
            return HTTPFound(location=url)
        config.add_view(redirect, route_name=name + '-auto')
    
    
    