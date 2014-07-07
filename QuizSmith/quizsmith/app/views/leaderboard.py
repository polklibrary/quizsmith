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
from pyramid.view import view_config
from pyramid.url import route_url
from quizsmith.app.views import BaseView
from quizsmith.app.utilities import ACL,Result2Dict,Seconds2Str
from quizsmith.app.models import DBSession,Tests,Users,Properties
import datetime, math, time, urllib2, json

class LeaderBoard(BaseView):


    mapper = {'0' : 'total_competitive',
              '1' : 'total_competitive',
              '2' : 'time_spent',
              '3' : 'users_id',
             }

    @view_config(route_name='leaderboard', permission=ACL.ANONYMOUS)
    def leaderboard(self):
        category = urllib2.unquote(self.request.params.get('category',''))
        self.response['active_category'] = category
        self.response['categories'] = LeaderBoard.categories()
        return self.template('leaderboard.pt')

        
    @view_config(route_name='leaderboardYourScore', renderer='json', permission=ACL.PLAY)
    def leaderboardYourScore(self):
        try:
            category = urllib2.unquote(self.request.params.get('category','0'))
            if category == '0':
                best = Tests.by({'alias':self.request.user.alias, 'completed':1}, sort='total_competitive desc').filter(Tests.created>=LeaderBoard.archive_date()).first()
                result = LeaderBoard.get_all_ranking(best)
            else:
                best = Tests.by({'category':category, 'alias':self.request.user.alias, 'completed':1}, sort='total_competitive desc').filter(Tests.created>=LeaderBoard.archive_date()).first()
                result = LeaderBoard.get_ranking(best)
            return {'status': True, 'rank': result['ranking'], 'total_competitive': result['total_competitive'], 'time_spent': Seconds2Str(result['time_spent']),
                    'total_time': Seconds2Str(best.total_time)}
        except Exception as e:
            return {'status': False}
        
        
    @view_config(route_name='leaderboardScores', renderer='json', permission=ACL.ANONYMOUS)
    def leaderboardScores(self):
        category = urllib2.unquote(self.request.params.get('category','0'))
        
        if 'iSortCol_0' in self.request.params:
            by = self.mapper[ self.request.params['iSortCol_0'] ]
            sort = self.request.params['sSortDir_0']
        
        if category == '0':
            results = LeaderBoard.all_categories(by=by, sort=sort,
                                                 limit=self.request.params['iDisplayLength'],
                                                 offset=self.request.params['iDisplayStart'])
            records = LeaderBoard.all_counts()
        else:
            results = LeaderBoard.category(category, by=by, sort=sort,
                                                 limit=self.request.params['iDisplayLength'],
                                                 offset=self.request.params['iDisplayStart'])
            records = LeaderBoard.counts(category)
        
        
        ranking = -records
        if sort == 'desc':
            ranking = 1 + int(self.request.params.get('iDisplayStart',0))
        
        rows = []
        for i, result in enumerate(results):            
            rows.append([ math.fabs(i+ranking),
                         result.total_competitive,
                         Seconds2Str(result.time_spent),
                         Seconds2Str(result.total_time),
                         result.alias
                        ])
            
        json = {
              "sEcho": int(time.time()),
              "iTotalRecords": records,
              "iTotalDisplayRecords": records,
              "aaData" : rows
            }
            
        return json
        
    @view_config(route_name='leaderboard_top_scores', permission=ACL.ANONYMOUS)
    def leaderboard_top_scores(self):
        self.response['hofs'] = json.loads(Properties.get('LEADERBOARD_HOF','[]'))
        return self.template('leaderboard_top.pt')
        
        
    @classmethod
    def category(cls, category, by='id', sort='asc', limit=1000,offset=0):
        sq = DBSession.query(Tests).filter(Tests.category==category).filter(Tests.completed==1).filter(Tests.created>=LeaderBoard.archive_date()).order_by('total_competitive desc').subquery()
        sq2 = DBSession.query(Tests).select_from(sq).group_by('alias').subquery()
        return DBSession.query(Tests).select_from(sq2).order_by(by + ' ' + sort).offset(offset).limit(limit).all()
        
    @classmethod
    def counts(cls,category):
        return DBSession.query(Tests).filter(Tests.category==category).filter(Tests.completed==1).filter(Tests.created>=LeaderBoard.archive_date()).group_by('alias').count()
        
    @classmethod
    def categories(cls):
        return DBSession.query(Tests).group_by('category').order_by('category asc')
        
    @classmethod
    def all_categories(cls,by='id',sort='asc',limit=1000,offset=0):
        sq = DBSession.query(Tests).filter(Tests.completed==1).filter(Tests.created>=LeaderBoard.archive_date()).order_by('total_competitive desc').subquery()
        sq2 = DBSession.query(Tests).select_from(sq).group_by('alias').subquery()
        return DBSession.query(Tests).select_from(sq2).order_by(by + ' ' + sort).limit(limit).offset(offset).all()
        
    @classmethod
    def all_counts(cls,by='id',sort='asc',limit=1000,offset=0):
        return DBSession.query(Tests).filter(Tests.completed==1).filter(Tests.created>=LeaderBoard.archive_date()).group_by('alias').count()
        
    @classmethod
    def get_ranking(cls,test):
        sq = DBSession.query(Tests).filter(Tests.category==test.category).filter(Tests.completed==1).filter(Tests.created>=LeaderBoard.archive_date()).order_by('total_competitive desc').subquery()
        results = DBSession.query(Tests).select_from(sq).filter(Tests.total_competitive > test.total_competitive).group_by('alias').all()
        data = Result2Dict(test)
        data['ranking'] = len(results) + 1  #prevent zero rank
        return data  
        
    @classmethod
    def get_all_ranking(cls,test):
        sq = DBSession.query(Tests).filter(Tests.completed==1).filter(Tests.created>=LeaderBoard.archive_date()).order_by('total_competitive desc').subquery()
        results = DBSession.query(Tests).select_from(sq).filter(Tests.total_competitive > test.total_competitive).group_by('alias').all()
        data = Result2Dict(test)
        data['ranking'] = len(results) + 1  #prevent zero rank
        return data  
        
    @classmethod
    def archive_date(cls):
        return datetime.datetime.strptime(Properties.get('LEADERBOARD_ARCHIVE_DATE'), '%Y-%m-%d')
        
        