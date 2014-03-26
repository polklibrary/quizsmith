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

from pyramid.httpexceptions import HTTPForbidden
from pyramid.view import view_config
from quizsmith.addons.d2l.integration import D2L
from quizsmith.app.models import Tests, Users, Categories

import d2lvalence.auth as d2lauth
import d2lvalence.service as d2lservice


class D2LInstructorGrades(D2L):

    @view_config(route_name='d2l_instructor_grades')
    def d2l_instructor_grades(self):
        uc = self.get_user_context()
        if not isinstance(uc, d2lauth.D2LUserContext):
            return uc # if no user_context is setup, return uc to d2l to get authorized.
        
        try:
            students = []
            category = self.request.params.get('category','---')
            
            if category != '---':
                id = self.request.matchdict['id']
                classlist = d2lservice.get_classlist(uc,org_unit_id=id)
                
                for student in classlist:
                    email = str(student.props['Username']) + self.settings('d2l_append_email_address','')
                    student_summary = {'name': str(student.props['DisplayName']),
                                       'email': email,
                                       'bestgrade' : 'Incomplete',
                                      }
                    
                    user = Users.by({'email':email}).first()
                    if user:
                        test = Tests.by({'alias':user.alias,'category':category}, sort='total_percentage desc').first()
                        if test:
                            student_summary['bestgrade'] = str(test.percentage) + '%'
                    
                    students.append(student_summary)
                
            self.response['students'] = students
            self.response['categories'] = Categories.all()
            return self.template('instructors-grades.pt', theme='D2L') 
        except Exception as e:
            print "ERROR: " + str(e) # log later?
        return HTTPForbidden() 

