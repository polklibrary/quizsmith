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

from quizsmith.app.utilities import add_route
from quizsmith.setup import Addons

Addons.register('QuizSmith Core','1.0.0')
def addon(config):

    # App Routes
    config.add_route('menu', '/') #root
    add_route(config, 'help', '/help')
    add_route(config, 'feedback', '/help/feedback')
    add_route(config, 'credits', '/credits')
    add_route(config, 'profile', '/profile')
    add_route(config, 'change_password', '/profile/change')
    add_route(config, 'halt', '/halt')
    add_route(config, 'login', '/login')
    add_route(config, 'logout', '/logout')
    add_route(config, 'register', '/register')
    add_route(config, 'alias', '/alias')
    add_route(config, 'category', '/category')
    add_route(config, 'category_intro', '/category/{id}')
    add_route(config, 'playing', '/category/{id}/playing')
    add_route(config, 'accessibility', '/category/{id}/playing/accessibility')
    add_route(config, 'next', '/category/{id}/playing/next')
    add_route(config, 'check', '/category/{id}/playing/check')
    add_route(config, 'result', '/category/{id}/playing/result')
    add_route(config, 'score', '/profile/score/{id}')
    add_route(config, 'pdf', '/profile/pdf/{id}.pdf')
    add_route(config, 'email', '/profile/email/{id}')
    add_route(config, 'leaderboard', '/leaderboard')
    add_route(config, 'leaderboardScores', '/leaderboardScores')
    add_route(config, 'leaderboardYourScore', '/leaderboardYourScore')
    add_route(config, 'leaderboard_top_scores', '/leaderboard/top')

    config.include('pyramid_mailer') # Mailer
    config.scan()
    return config

