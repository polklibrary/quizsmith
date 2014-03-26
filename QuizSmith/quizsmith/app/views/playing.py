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
from pyramid.view import view_config
from pyramid.url import route_url
from quizsmith.app.views import BaseView
from quizsmith.app.utilities import ACL,TestCreator,TestManager,Result2Dict
from quizsmith.app.models import DBSession,Categories,QuestionSets,Tests,TestsResults,Transitions,Users,Answers
import random, transaction, time, urllib2

class Playing(BaseView):


    def _secure_get_category(self,id):
        category = Categories.by(id, user=self.request.user, permission=ACL.PLAY).first()
        if category:
            return category
        raise HTTPForbidden()

    @view_config(route_name='playing', permission=ACL.AUTHENTICATED)
    def playing(self):
        id = int(self.request.matchdict['id'])
        category = self._secure_get_category(id)
        if category:
            use_accessibility_view = self.request.user.needs_accessibility
            TestCreator(self.request.user, category.id)
            if use_accessibility_view:
                return HTTPFound(location=route_url('accessibility', self.request, id=id))
            self.response['category'] = Categories.by(id).first()
            return self.template('playing.pt')
    
    
    @view_config(route_name='next', renderer='json', permission=ACL.AUTHENTICATED)
    def next(self):
        id = int(self.request.matchdict['id'])
        category = self._secure_get_category(id)
        self.response['finished'] = False
        result = TestsResults.by({'tests_id':self.request.user.current_test, 'attempted':False}, sort='id asc').first()
        
        if result:
            c = Categories.by(id, user=self.request.user, permission=ACL.PLAY).first()
            self.response['category'] = Result2Dict(c, purge=['category_intro'])
            self.response['category']['transition_in'] = Result2Dict(c.get_transition_in())
            self.response['category']['transition_out'] = Result2Dict(c.get_transition_out())
            self.response['question'] = result.question
            #self.response['answers'] = TestManager.get_answers(result.question_sets_id)
            self.response['answers'] = result.get_answers()
            
            result.attempted = True
            user = Users.by(self.request.user.id).first()
            user.current_question = result.question_sets_id
            transaction.commit()
        else:
            test = Tests.by(self.request.user.current_test).first()
            self.response['test_id'] = self.request.user.current_test
            test.completed = True
            transaction.commit()
            self.response['finished'] = True
            
        return self.response
        
        
    @view_config(route_name='check', renderer='json', permission=ACL.AUTHENTICATED)
    def check(self):
        self.response['was_correct'] = -1
        category = self._secure_get_category(int(self.request.matchdict['id']))
        
        if 'answer' in self.request.params:
            answer = self.request.params.get('answer','0')
            duration = float(self.request.params['time'])
            self.response['was_correct'] = TestManager.check_answer_byid(self.request.user.current_question, answer)
            
            result = TestsResults.by({'tests_id':self.request.user.current_test, 'question_sets_id':self.request.user.current_question}).first()
            test = Tests.by(self.request.user.current_test).first()

            if not self.response['was_correct'] and duration > 0:
                if result.wrong_attempts < test.max_wrong_answer_allowed:
                    result.wrong_attempts += 1
                    duration = duration - test.wrong_answer_time_penalty
            
            # cheaters hacking more than duration will result in failure
            if duration <= 0 or duration > test.question_time_allowed:
                duration = 0

            self.response['continue_on'] = True
            if result.wrong_attempts == test.max_wrong_answer_allowed or self.response['was_correct'] or duration == 0:
                self.response['continue_on'] = False
                
            result.correctly_answered = self.response['was_correct']
            result.duration = duration
            answers = result.get_answers()
            changed = []
            for a in answers:
                if a['id'] == int(answer):
                    checked = -1
                    if self.response['was_correct']:
                        checked = 1
                    changed.append({'id':a['id'],'content':a['content'],'answered':checked})
                else:
                    changed.append(a)
            result.set_answers(changed)
            transaction.commit()
            
        self.response['duration'] = int(duration)
        return self.response
        
        
    @view_config(route_name='result', renderer='json', permission=ACL.AUTHENTICATED)
    def result(self):
        from quizsmith.app.views.leaderboard import LeaderBoard
        category = self._secure_get_category(int(self.request.matchdict['id']))
        
        self.response['question'] = None
        self.response['wrong_attempts'] = 0
        self.response['duration'] = 0
    
        test = Tests.by(self.request.user.current_test).first()
        result = TestsResults.by({'tests_id':self.request.user.current_test, 'attempted':True}, sort='id desc').first()
        results = TestsResults.by({'tests_id':self.request.user.current_test}).all()
        questionset = QuestionSets.by(result.question_sets_id).first()
        
        self.response['answer_help'] = questionset.answer_help
        self.response['result'] = Result2Dict(result,purge=['id','tests_id','question_sets_id'])
        final = self._test_calculator(test,results,result)
        self.response['percentage'] = final['percentage']
        self.response['competitive'] = final['competitive']
        self.response['ranking'] = LeaderBoard.get_ranking(test)
        transaction.commit()
            
        return self.response
        
        
    @view_config(route_name='accessibility', permission=ACL.AUTHENTICATED)
    def accessibility_view(self):
        category = self._secure_get_category(int(self.request.matchdict['id']))
        
        if self.request.params.get('nojs','0') != '1':
            if not self.request.user.needs_accessibility:
                return HTTPFound(location=route_url('category', self.request))
    
        id = self.request.user.current_test
        test = Tests.by(id).first()
        results = TestsResults.by({'tests_id':id}, sort='id asc').all()
    
        if 'form.submit' in self.request.params:
            for key, value in self.request.params.iteritems():
                key_type, sep, rid = key.rpartition(".")
                if key_type == 'question':
                    result = TestsResults.by(rid).first()
                    passed = TestManager.check_answer_byid(result.question_sets_id, int(value))
                    result.correctly_answered = passed
                    if not passed:
                        result.wrong_attempts = test.max_wrong_answer_allowed
                    result.attempted = True
                    result.duration = self._accessibility_duration_calculator(self.request.params['st'], len(results), test.question_time_allowed)
                    final = self._test_calculator(test,results,result)
            transaction.commit()
            return HTTPFound(location=route_url('score', self.request, id=id))
        else:
            self.response['time_started'] = int(time.time())
            self.response['test'] = test
            self.response['results'] = []
            for result in results:
                self.response['results'].append({'question_set': result,
                                                 'answer': result.get_answers()})
            return self.template('playing-accessibility.pt')
    
    
    def _test_calculator(self,test,results,result):
        percentage = TestManager.score_percentage(result.correctly_answered,
                                                    result.wrong_attempts,
                                                    test.max_wrong_answer_allowed,
                                                    len(results),
                                                    result.duration,
                                                    test.question_time_allowed
                                                    )
        competitive = TestManager.score_competitive(result.correctly_answered,
                                                    result.wrong_attempts,
                                                    test.max_wrong_answer_allowed,
                                                    len(results),
                                                    result.duration,
                                                    test.question_time_allowed
                                                    )
        
        test.total_percentage += percentage
        test.base_competitive += competitive['score']
        test.bonus_competitive += competitive['bonus']
        test.total_competitive += competitive['combined']
        test.time_remaining += result.duration
        test.time_spent += (test.question_time_allowed - result.duration)
        DBSession.flush()
        return { 'competitive': competitive, 'percentage': percentage }
        
        
    def _accessibility_duration_calculator(self, start, question_amount, total_time_allowed):
        """ This isn't ideal, but it is a start """
        length = int(time.time()) - int(start)
        t = length/question_amount
        final = total_time_allowed - t
        if final == 0:
            final = random.randint(1,15)
        return final

    