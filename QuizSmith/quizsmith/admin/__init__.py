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

from quizsmith.app.utilities import PyramidFormalchemyACL, add_route
from quizsmith.app.views import BaseView
from quizsmith.app.models import Categories
from quizsmith.app.utilities import ACL
from quizsmith.setup import Addons

Addons.register('QuizSmith Admin Panel','1.0.0')
def addon(config):

    # Edit Panel Routes
    add_route(config, 'edit_home','/edit')
    add_route(config, 'edit_categories','/edit/categories')
    add_route(config, 'edit_info', '/edit/info')
    add_route(config, 'import_category', '/edit/category/import')
    add_route(config, 'edit_category','/edit/category/{category}')
    add_route(config, 'edit_questions', '/edit/category/{category}/questions')
    add_route(config, 'edit_question','/edit/category/{category}/questions/{id}')
    add_route(config, 'export_category', '/edit/category/{category}/export/{category_name}.zip')
    add_route(config, 'edit_delete', '/edit/delete/{type}/{id}')
    add_route(config, 'edit_groups', '/edit/groups')
    add_route(config, 'edit_theme', '/edit/theme')
    add_route(config, 'export_theme', '/edit/theme/export/{theme_name}.zip')
    add_route(config, 'edit_mailer', '/edit/mailer')
    add_route(config, 'edit_leaderboard', '/edit/leaderboard')
    add_route(config, 'edit_reports', '/edit/reports')
    add_route(config, 'edit_reports_problematic_questions', '/edit/reports/problematic-questions')
    add_route(config, 'edit_report_avg_score', '/edit/reports/average-score')
    
    # Admin Scaffold Configuration
    config.include('pyramid_fanstatic')
    config.include('pyramid_formalchemy')
    config.include('fa.jquery')
    config.formalchemy_admin('/admin', package='quizsmith.app', view='fa.jquery.pyramid.ModelView',factory=PyramidFormalchemyACL)
    config.formalchemy_model('/properties', package='quizsmith.app', view='fa.jquery.pyramid.ModelView', model='quizsmith.app.models.Properties')
    config.formalchemy_model('/users', package='quizsmith.app', view='fa.jquery.pyramid.ModelView', model='quizsmith.app.models.Users')
    config.formalchemy_model('/groups', package='quizsmith.app', view='fa.jquery.pyramid.ModelView', model='quizsmith.app.models.Groups')
    config.formalchemy_model('/categories', package='quizsmith.app', view='fa.jquery.pyramid.ModelView', model='quizsmith.app.models.Categories')
    config.formalchemy_model('/questionsets', package='quizsmith.app', view='fa.jquery.pyramid.ModelView', model='quizsmith.app.models.QuestionSets')
    config.formalchemy_model('/questions', package='quizsmith.app', view='fa.jquery.pyramid.ModelView', model='quizsmith.app.models.Questions')
    config.formalchemy_model('/answers', package='quizsmith.app', view='fa.jquery.pyramid.ModelView', model='quizsmith.app.models.Answers')
    config.formalchemy_model('/transitions', package='quizsmith.app', view='fa.jquery.pyramid.ModelView', model='quizsmith.app.models.Transitions')
    config.formalchemy_model('/tests', package='quizsmith.app', view='fa.jquery.pyramid.ModelView', model='quizsmith.app.models.Tests')
    config.formalchemy_model('/testsresults', package='quizsmith.app', view='fa.jquery.pyramid.ModelView', model='quizsmith.app.models.TestsResults')
    
    config.scan()
    return config


class EditBaseView(BaseView):

    def __init__(self, request):
        super(EditBaseView, self).__init__(request)
        self.response['categories'] = Categories.by(None, sort='position asc', user=self.request.user, permission=ACL.EDIT)
      
