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

from pyramid.httpexceptions import HTTPFound,HTTPNotFound,HTTPForbidden
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.url import route_url
from pyramid_mailer import get_mailer
from pyramid_mailer.message import Attachment,Message
from sqlalchemy import exc
from quizsmith.app.views import BaseView
from quizsmith.app.utilities import ACL,TestManager,Seconds2Str,Validate,RemoveImages
from quizsmith.app.models import DBSession,Tests,TestsResults,Categories,QuestionSets,Properties
import transaction, random, random, StringIO
import ho.pisa as pisa

class Score(BaseView):

    @view_config(route_name='score', permission=ACL.AUTHENTICATED)
    def score(self):
        id = self.request.matchdict['id']
        test = Tests.by(id).first()
        
        if not test:
            raise HTTPNotFound()
            
        elif test.alias == self.request.user.alias:
            results = TestsResults.by({'tests_id':id}, sort='id asc').all()
            self.response['test'] = test
            self.response['test_total_time'] = Seconds2Str(test.time_spent)
            self.response['librarian'] = test.id % 2 == 0
            self.response['results'] = []
            total = len(results)
            
            self.response['category'] = None
            self.response['assessment'] = None
            try:
                category = Categories.by({'name':test.category}).first()
                self.response['category'] = category
                self.response['assessment'] = category.assess_this(test.percentage)
            except exc.SQLAlchemyError as e: 
                pass # defensive
        
            for result in results:
                self.response['results'].append( self.get_question_scores(result, 
                                                                          total, 
                                                                          test.max_wrong_answer_allowed, 
                                                                          test.question_time_allowed
                                                                          ))
        else:
            raise HTTPForbidden()
        
        return self.template('score.pt')
        
        
    def get_question_scores(self, result, total_results, max_allowed_wrong, max_allowed_duration):
    
        percentage = TestManager.score_percentage(result.correctly_answered,
                                                     result.wrong_attempts,
                                                     max_allowed_wrong,
                                                     total_results,
                                                     result.duration,
                                                     max_allowed_duration
                                                     )
        competitive = TestManager.score_competitive(result.correctly_answered,
                                                     result.wrong_attempts,
                                                     max_allowed_wrong,
                                                     total_results,
                                                     result.duration,
                                                     max_allowed_duration
                                                     )
                                                     
        answer_help = None
        try:
            try:
                # if questionset was removed, this will still allow people to view old tests.
                answer_help = QuestionSets.by(result.question_sets_id).first().answer_help
            except exc.SQLAlchemyError as e:
                pass # defensive
        except Exception as e:
            pass # defensive
                
        return { 'question' : str(result.question),
                 'question_textonly' : RemoveImages(result.question),
                 'correctly_answered' : result.correctly_answered,
                 'wrong_attempts' : result.wrong_attempts,
                 'duration' : result.duration,
                 'duration_passed_fmt' : Seconds2Str((max_allowed_duration-result.duration)),
                 'duration_remaining_fmt' : Seconds2Str(result.duration),
                 'percentage' : percentage,
                 'competitive' : competitive,             
                 'answer_help': str(answer_help),           
                 'attempted': result.attempted,    
                 'answer_choices': str(result.get_answers()),
                 'had_wrong_attempts': (result.wrong_attempts!=0 and result.attempted),
                 'had_more_than_one_wrong': (result.wrong_attempts>1),
                 'had_no_time_remaining': (result.duration<1 and result.attempted),
                }
                
        
        
    @view_config(route_name='pdf', permission=ACL.AUTHENTICATED)
    def pdf(self):
        id = self.request.matchdict['id']
        file = self._generate_pdf(id)
        
        if not file:
            raise HTTPForbidden()
        else:
            response = Response(content_type='application/pdf')
            response.write(file)
            return response
            
    def _generate_pdf(self, id):
        test = Tests.by({'id':id,'alias':self.request.user.alias}).first()
        if not test:
            return None
        elif test.alias == self.request.user.alias:
            self.response['test'] = test
            self.response['results'] = []                           
            self.response['total_correct'] = 0
            results = TestsResults.by({'tests_id':id}).all()
            total = len(results)
            for result in results:
                self.response['results'].append( self.get_question_scores(result, 
                                                                          total,
                                                                          test.max_wrong_answer_allowed, 
                                                                          test.question_time_allowed 
                                                                          ))
                if bool(result.correctly_answered):
                    self.response['total_correct'] += 1
                                    
            self.response['category'] = None
            self.response['assessment'] = None
            try:
                category = Categories.by({'name':test.category}).first()
                self.response['category'] = category
                self.response['assessment'] = category.assess_this(test.percentage)
            except exc.SQLAlchemyError as e: 
                pass # defensive
                
            pdf_html = self.template('pdf.pt')
            io = StringIO.StringIO()
            pisa.pisaDocument(StringIO.StringIO( pdf_html.text.encode( "UTF-8" )), io)
            return io.getvalue()
        else:
            return None
            
            
    @view_config(route_name='email', permission=ACL.AUTHENTICATED)
    def email(self):
        id = self.request.matchdict['id']
        test = Tests.by({'id':id,'alias':self.request.user.alias}).first()
        if not test:
            raise HTTPForbidden()
        file = self._generate_pdf(id)
        self.response['id'] = id
        self.response['emails'] = self.request.params.get('email.addresses',None)
        
        if 'form.submitted' in self.request.params:
            if self.request.params['email.ok'] == '1':
                emails = self.request.params['email.addresses'].replace(' ','').split(',')
                for email in emails:
                    if not Validate.email(email):
                        self.notify('Invalid email address',warn=True)
                        return self.template('email.pt')
                        
                try:
                    message = Message(subject=self._email_fmt(id, str(Properties.get('MAILER_TO_SUBJECT','Submission'))),
                                      sender=str(Properties.get('MAILER_GLOBAL_FROM_ADDRESS','System')),
                                      recipients=emails,
                                      body=self._email_fmt(id, str(Properties.get('MAILER_BODY','Submission'))))
                    attachment = Attachment('submission_' + str(id) + '.pdf', 'application/pdf', file)
                    message.attach(attachment)
                    mailer = get_mailer(self.request)
                    mailer.send(message)
                    self.notify('Email sent!')
                except Exception as e:
                    print "ERROR: " + str(e)
                    self.notify('Unable to send email!',warn=True)
            else:
                self.notify('Unable to send example email!',warn=True)

        return self.template('email.pt')
            
            
    def _email_fmt(self,id,text):
        test = Tests.by(id).first()
        text = text.replace('${CATEGORY}', test.category)
        text = text.replace('${ALIAS}', test.alias)
        return text
            