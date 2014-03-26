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

from paste.deploy import loadapp
from paste.deploy.loadwsgi import appconfig
from pyramid import testing
from pyramid.config import Configurator
from quizsmith.app.models import DBSession, Users, Categories
from sqlalchemy import engine_from_config
from webtest import TestApp

import unittest, os, transaction, pyramid.registry, pyramid.request

ini = 'config:' + os.path.join(os.path.dirname(__file__), '../', 'development.ini')
settings = appconfig(ini)


#Run testes with: python QuizSmith/setup.py test

class AnoynmousPermissionTests(unittest.TestCase):

    category = 1

    def setUp(self):
        reg = pyramid.registry.Registry('testing')
        wsgiapp = self._load_wsgiapp()
        self.config = Configurator(registry=wsgiapp.registry, package='quizsmith')
        self.config.setup_registry(settings=settings)
        self.app = TestApp(wsgiapp, extra_environ={})
        
        category = Categories.newest().id
        
    def tearDown(self):
        self.config.end()
        
    def _load_wsgiapp(self):
        wsgiapp = loadapp(ini)
        return wsgiapp
        
    def _get_app_url(self):
        return 'http://0.0.0.0:6543'
    
        
    """ NOT LOGGED ALLOWED IN BELOW """   
    def test_menu(self):
        res = self.app.get('/', status=200)
        self.assertTrue(res.status_code==200)
    
    def test_leaderboard(self):
        res = self.app.get('/leaderboard', status=200)
        self.assertTrue(res.status_code==200)
        
    def test_leaderboard_scores(self):
        res = self.app.get('/leaderboardScores?category=0&iDisplayLength=1&iDisplayStart=0&iSortCol_0=0&sSortDir_0=asc', status=200)
        self.assertTrue(res.status_code==200)
        
    def test_not_found(self):
        res = self.app.get('/random/location/3llt', status=404)
        self.assertTrue(res.status_code==404)
        
        
    """ NOT LOGGED NOT ALLOWED IN BELOW """
    def test_alias_not_logged_in(self):
        res = self.app.get('/alias', status=403)
        self.assertTrue(res.status_code==403)
        
    def test_playing_not_logged_in(self):
        res = self.app.get('/category/1/playing', status=403)
        self.assertTrue(res.status_code==403)
        
    def test_playing_accessability_not_logged_in(self):
        res = self.app.get('/category/1/playing/accessibility', status=403)
        self.assertTrue(res.status_code==403)
        
    def test_playing_next_not_logged_in(self):
        res = self.app.get('/category/1/playing/next', status=403)
        self.assertTrue(res.status_code==403)
        
    def test_playing_check_not_logged_in(self):
        res = self.app.get('/category/1/playing/check', status=403)
        self.assertTrue(res.status_code==403)
        
    def test_playing_result_not_logged_in(self):
        res = self.app.get('/category/1/playing/result', status=403)
        self.assertTrue(res.status_code==403)
        
    def test_alias_not_logged_in(self):
        res = self.app.get('/alias', status=403)
        self.assertTrue(res.status_code==403)
        
    def test_category_intro_not_logged_in(self):
        res = self.app.get('/category/1', status=403)
        self.assertTrue(res.status_code==403)
        
    def test_category_not_logged_in(self):
        res = self.app.get('/category', status=403)
        self.assertTrue(res.status_code==403) 
        
    def test_leaderboard_your_scores(self):
        res = self.app.get('/leaderboardYourScore', status=403)
        self.assertTrue(res.status_code==403)
        
    def test_profile_not_logged_in(self):
        res = self.app.get('/profile', status=403)
        self.assertTrue(res.status_code==403) 
        
    def test_profile_score_not_logged_in(self):
        res = self.app.get('/profile/score/1', status=403)
        self.assertTrue(res.status_code==403)   
        
    def test_profile_email_not_logged_in(self):
        res = self.app.get('/profile/email/1', status=403)
        self.assertTrue(res.status_code==403)   
        
    def test_profile_pdf_not_logged_in(self):
        res = self.app.get('/profile/pdf/1.pdf', status=403)
        self.assertTrue(res.status_code==403)   
        
    """ ADMIN STUFF BELOW """
    def test_admin_not_logged_in(self):
        res = self.app.get('/admin/', status=403)
        self.assertTrue(res.status_code==403)    
        
    def test_edit_not_logged_in(self):
        res = self.app.get('/edit', status=403)
        self.assertTrue(res.status_code==403)
        
        res = self.app.get('/edit/groups', status=403)
        self.assertTrue(res.status_code==403)
        
        res = self.app.get('/edit/assessments', status=403)
        self.assertTrue(res.status_code==403)        
        
        res = self.app.get('/edit/properties', status=403)
        self.assertTrue(res.status_code==403)     
        
        res = self.app.get('/edit/info', status=403)
        self.assertTrue(res.status_code==403)     
        
        res = self.app.get('/edit/category/1', status=403)
        self.assertTrue(res.status_code==403)     
        
        res = self.app.get('/edit/category/1/questions', status=403)
        self.assertTrue(res.status_code==403)
        
        res = self.app.get('/edit/category/1/questions/1', status=403)
        self.assertTrue(res.status_code==403)
        
        res = self.app.get('/edit/category/import', status=403)
        self.assertTrue(res.status_code==403)
        
        res = self.app.get('/edit/delete/Categories/1?back=http://www.google.com', status=403)
        self.assertTrue(res.status_code==403)
        
        
class PlayerPermissionTests(AnoynmousPermissionTests):

    auto_increment_reset = 0
    
    def setUp(self):
        super(PlayerPermissionTests,self).setUp()
        Users.registerLocalUser(email='player@test.com', password='testplayer')
        user = Users.by({'email':'player@test.com'}).first()
        self.auto_increment_reset = user.id
        
    def tearDown(self):
        user = Users.by({'email':'player@test.com'}).first()
        DBSession.delete(user)
        DBSession.flush()
        DBSession.execute("ALTER TABLE users AUTO_INCREMENT = " + str(self.auto_increment_reset) + ";")
        transaction.commit()
        super(PlayerPermissionTests,self).tearDown()

    def _run_login(self):
        return self.app.get('/login?local=1&email=player@test.com&password=testplayer&form.submitted=1', status=302)
    
    def _run_alias_creator(self):
        self._run_login()
        return self.app.get('/alias?alias=TEST&form.submitted=1', status=302)
        
    """ PLAYER PERSMISSION LOGGED IN BELOW """
    def test_player_login(self):
        res = self._run_login()
        self.assertTrue(res.status_code==302) # redirect means passed   
        self.assertFalse(res.status_code==200) # return means failed  
        
    def test_player_alias(self):
        self._run_login()
        res = self.app.get('/alias', status=200)
        self.assertTrue(res.status_code==200)   
        
    def test_player_alias_creation(self):
        res = self._run_alias_creator()
        self.assertTrue(res.status_code==302) # redirect means passed   
        self.assertFalse(res.status_code==200) # return means failed  
        
    def test_player_category_list(self):
        self._run_alias_creator()
        res = self.app.get('/category', status=200)
        self.assertTrue(res.status_code==200)  
        
    def test_player_category_introduction(self):
        self._run_alias_creator()
        res = self.app.get('/category/1', status=200)
        self.assertTrue(res.status_code==200)  
        
    def test_player_playing_routine(self):
        self._run_alias_creator()
        
        #start
        res = self.app.get('/category/1/playing', status=200)
        self.assertTrue(res.status_code==200)  
        
        #next question
        res = self.app.get('/category/1/playing/next', status=200)
        self.assertTrue(res.status_code==200)  
        self.assertTrue("category" in res.body)  
        self.assertTrue("wrong_answer_time_penalty" in res.body)  
        self.assertTrue("transition_in" in res.body)  
        self.assertTrue("transition_out" in res.body)  
        
        #check answer
        res = self.app.get('/category/1/playing/check?answer=1&time=5', status=200)
        self.assertTrue(res.status_code==200)  
        self.assertTrue("duration" in res.body)  
        self.assertTrue("continue_on" in res.body)  
        self.assertTrue("was_correct" in res.body)
        
        #result
        res = self.app.get('/category/1/playing/result', status=200)
        self.assertTrue(res.status_code==200) 
        self.assertTrue("ranking" in res.body)  
        self.assertTrue("category" in res.body)  
        self.assertTrue("competitive" in res.body)
        self.assertTrue("percentage" in res.body)
        self.assertTrue("answer_help" in res.body)
        
        #get user
        user = Users.by({'email':'player@test.com'}).first()
        
        #score
        res = self.app.get('/profile/score/' + str(user.current_test), status=200)
        self.assertTrue(res.status_code==200) 
        
        #NOTE: I can't figure out the PDF generation tests.
        
    def test_player_profile(self):
        self._run_alias_creator()
        res = self.app.get('/profile', status=200)
        self.assertTrue(res.status_code==200)
    
    
    # RESTRICTED AREAS NOT ALLOWED BY PLAYER BELOW
    def test_player_admin(self):
        self._run_alias_creator()
        res = self.app.get('/admin/', status=403)
        self.assertTrue(res.status_code==403)
        
    def test_player_edit(self):
        self._run_alias_creator()
        res = self.app.get('/edit', status=403)
        self.assertTrue(res.status_code==403)
        
        res = self.app.get('/edit/groups', status=403)
        self.assertTrue(res.status_code==403)
        
        res = self.app.get('/edit/assessments', status=403)
        self.assertTrue(res.status_code==403)        
        
        res = self.app.get('/edit/properties', status=403)
        self.assertTrue(res.status_code==403)     
        
        res = self.app.get('/edit/info', status=403)
        self.assertTrue(res.status_code==403)     
        
        res = self.app.get('/edit/category/1', status=403)
        self.assertTrue(res.status_code==403)
        
        res = self.app.get('/edit/category/1/questions', status=403)
        self.assertTrue(res.status_code==403)
        
        res = self.app.get('/edit/category/1/questions/1', status=403)
        self.assertTrue(res.status_code==403)
        
        res = self.app.get('/edit/category/import', status=403)
        self.assertTrue(res.status_code==403)
        
        res = self.app.get('/edit/delete/Categories/1?back=http://www.google.com', status=403)
        self.assertTrue(res.status_code==403)
        
      
class NoGroupPermissionTests(AnoynmousPermissionTests):

    auto_increment_reset = 0
    
    def setUp(self):
        super(NoGroupPermissionTests,self).setUp()
        Users.registerLocalUser(email='player@test.com', password='testplayer', groups=[])
        user = Users.by({'email':'player@test.com'}).first()
        self.auto_increment_reset = user.id
        
    def tearDown(self):
        user = Users.by({'email':'player@test.com'}).first()
        DBSession.delete(user)
        DBSession.flush()
        DBSession.execute("ALTER TABLE users AUTO_INCREMENT = " + str(self.auto_increment_reset) + ";")
        transaction.commit()
        super(NoGroupPermissionTests,self).tearDown()

    def _run_login(self):
        return self.app.get('/login?local=1&email=player@test.com&password=testplayer&form.submitted=1', status=302)
    
    def _run_alias_creator(self):
        self._run_login()
        return self.app.get('/alias?alias=TEST&form.submitted=1', status=302)
        
    """ PLAYER PERSMISSION LOGGED IN BELOW """
    def test_no_group_login(self):
        res = self._run_login()
        self.assertTrue(res.status_code==302) # redirect means passed   
        self.assertFalse(res.status_code==200) # return means failed  
                
    def test_no_group_alias(self):
        self._run_login()
        res = self.app.get('/alias', status=200)
        self.assertTrue(res.status_code==200) 
        
    def test_no_group_alias_creation(self):
        res = self._run_alias_creator()
        self.assertTrue(res.status_code==302) # redirect means passed   
        self.assertFalse(res.status_code==200) # return means failed  
        
    def test_no_group_category(self):
        res = self._run_alias_creator()
        res = self.app.get('/category', status=200)
        self.assertTrue(res.status_code==200)
        
    def test_no_group_category_intro(self):
        res = self._run_alias_creator()
        res = self.app.get('/category/1', status=403)
        self.assertTrue(res.status_code==403) 
        
    def test_no_group_playing(self):
        res = self._run_alias_creator()
        res = self.app.get('/category/1/playing', status=403)
        self.assertTrue(res.status_code==403) 
        
        res = self.app.get('/category/1/playing/next', status=403)
        self.assertTrue(res.status_code==403) 
        
        res = self.app.get('/category/1/playing/check', status=403)
        self.assertTrue(res.status_code==403) 
        
        res = self.app.get('/category/1/playing/result', status=403)
        self.assertTrue(res.status_code==403) 
        
    def test_no_group_profile(self):
        res = self._run_alias_creator()
        res = self.app.get('/profile', status=200)
        self.assertTrue(res.status_code==200) 
        
    def test_no_group_score(self):
        res = self._run_alias_creator()
        res = self.app.get('/profile/score/1', status=403)
        self.assertTrue(res.status_code==403) 
        
    def test_no_group_edit(self):
        res = self._run_alias_creator()
        res = self.app.get('/edit', status=403)
        self.assertTrue(res.status_code==403)  
        
    def test_no_group_admin(self):
        res = self._run_alias_creator()
        res = self.app.get('/admin/', status=403)
        self.assertTrue(res.status_code==403)  
        
        
    