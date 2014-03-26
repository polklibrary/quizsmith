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

from pyramid.response import Response
from pyramid.view import view_config
from quizsmith.app.models import DBSession, Categories, QuestionSets, Questions, Answers, Transitions, Groups
from quizsmith.app.utilities.utility import Result2Dict
from quizsmith.app.utilities import ACL
from quizsmith.admin import EditBaseView
from quizsmith.setup import Addons
import json,StringIO,transaction,zipfile

class ExportImport(EditBaseView):

    @view_config(route_name='export_category', permission=ACL.EDIT)
    def export_category(self):
        category_id = int(self.request.matchdict['category'])
        
        category = Result2Dict(Categories.by(category_id).first())
        sa_qs = QuestionSets.by({'category_id':category_id}).all()
        question_sets = []
        for qs in sa_qs:
            questions = []
            answers = []
            
            # Get QuestionSet Transform
            d_qs = Result2Dict(qs)
            
            # Get All Questions in QuestionSet and Transform
            sa_q = Questions.by({'question_sets_id':qs.id}).all()
            for q in sa_q:
                questions.append(Result2Dict(q))
            d_qs['questions'] = questions
            
            # Get All Answers in QuestionSet and Transform
            sa_a = Answers.by({'question_sets_id':qs.id}).all()
            for a in sa_a:
                answers.append(Result2Dict(a))
            d_qs['answers'] = answers
                
            question_sets.append(d_qs)
                
        return self._export_zip(json.dumps({'category' : category,
                                             'question_sets' : question_sets}, 
                                             sort_keys=True,
                                             indent=4, 
                                             separators=(',', ': ')
                                           ))
          

          
    @view_config(route_name='import_category', permission=ACL.EDIT)
    def import_category(self):        
    
        if 'form.submit' in self.request.params:
            content = self.request.params.get('form.import')
            data = self._import_zip(content)
            if not data:
                self.response['message'] = 'This export was made for a different version of this application.\
                                            You can rename the .zip filename to match your systems version, however this will most likely result in consequences and is not recommended.'
            else:
                category  = data['category']
                new_category = Categories(name=category['name'],
                           category_intro=category['category_intro'],
                           playable_questions=category['playable_questions'],
                           wrong_answer_time_penalty=category['wrong_answer_time_penalty'],
                           max_wrong_answer_allowed=category['max_wrong_answer_allowed'],
                           question_time_allowed=category['question_time_allowed'],
                           transition_in=category['transition_in'],
                           transition_out=category['transition_out'],
                           )
                
                new_category.set_groups([],[str(group.id) for group in Groups.by({'edit':True}).all()],[str(group.id) for group in Groups.by({'review':True}).all()]) #anyone with group edit permission are allowed to edit.
                DBSession.add(new_category)
                DBSession.flush()
                
                for qs in data['question_sets']:
                    new_qs = QuestionSets(category_id=new_category.id,
                                          answer_help=qs['answer_help']
                                         )
                    DBSession.add(new_qs)
                    DBSession.flush()
                    for q in qs['questions']:
                        new_q = Questions(question_sets_id=new_qs.id,
                                          question=q['question']
                                          ) 
                        DBSession.add(new_q)
                    for a in qs['answers']:
                        new_a = Answers(question_sets_id=new_qs.id,
                                        answer=a['answer'],
                                        position=a['position'],
                                        is_correct = a['is_correct']
                                        ) 
                        DBSession.add(new_a)
                DBSession.flush()
                transaction.commit()
                self.response['message'] = 'Imported!'
                self.response['message_class'] = 'info'
            
        return self.template('/import-category.pt', theme='AdminPanel')
        
        
    def _export_zip(self, obj):
        io = StringIO.StringIO()
        zf = zipfile.ZipFile(io, mode='w')
        zf.writestr('export.data', obj)
        zf.close()
        io.seek(0)
        file = io.read()
        io.close()
        return Response(content_type='application/zip', body=file)
        
    def _import_zip(self, obj):
        filename = obj.filename
        file = obj.file
        if not filename.endswith('-v' + Addons.get_version('QuizSmith Core') + '.zip'):
            return None
        zip = zipfile.ZipFile(file)
        data = zip.read('export.data')
        return json.loads(data)

    
    
    