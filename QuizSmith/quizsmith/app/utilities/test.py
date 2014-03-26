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

from quizsmith.app.models import DBSession,Categories,QuestionSets,Questions,Answers,Tests,TestsResults,Users
import transaction, random, operator

class TestManager(object):
    """ """
        
    @classmethod
    def get_answers(cls,id):
        answers = []
        
        wrong = Answers.by({'question_sets_id':id,'is_correct':False}).all()
        random.shuffle(wrong) # randomize wrong
        wrong = wrong[:3] # get max of first 3 wrong in randomized list
        correct = Answers.by({'question_sets_id':id,'is_correct':True}).first()
        answers = wrong + [correct] # add correct to list
        random.shuffle(answers) # randomize corect in list
        
        # sort em'. if all positions set as same value, all stay randomized from before.  cool eh?
        answers = sorted(answers, key=lambda a: a.position)  
        answer_set = []
        for a in answers:
            answer_set.append({'content':a.answer,'id':a.id,'answered':0})
        return answer_set
        
    @classmethod
    def check_answer_byid(cls,id,answer):
        correct_answer = Answers.by({'question_sets_id':id, 'is_correct':True}).first()
        return (correct_answer.id == int(answer))   
        
    @classmethod
    def score_percentage(cls,correct,attempts,max_attempts,total_questions,duration,total_duration):
        return (( float(max_attempts) - float(attempts)) / float(max_attempts)) * 100.0 * int(correct)
    
    @classmethod
    def score_competitive(cls,correct,attempts,max_attempts,total_questions,duration,total_duration):
        # With 2 attempts at 30 seconds max = 775 with a 60 bonus for 835
        # (maxattempts-attempts) * time (sqrt) * 100 * correct + ( maxattempts * duration )
        import math
        score = math.sqrt( (float(max_attempts) - float(attempts)) * duration ) * (100.0 * int(correct))
        bonus = (float(max_attempts) - float(attempts)) * float(duration)
        combined = score + bonus
        return {'score' : int(score), 'bonus' : int(bonus), 'combined': int(combined)}

        
class TestCreator(object):

    def __init__(self, user, category_id):
        self.alias = user.alias
        self.used_accessibility_view = user.needs_accessibility
        self.category_id = category_id
        self._generate_test()

    def _generate_test(self):
        category = Categories.by(self.category_id).first()
        last_test = Tests.by({'category':category.name, 'alias':self.alias},sort='id desc').first()
        
        # Create New Test
        test = Tests(alias=self.alias, category=category.name, d2l_folder=category.d2l_folder, used_accessibility_view=self.used_accessibility_view)
        # Copy values at time of generation, this in case values change in the future, personal results aren't effected.
        test.wrong_answer_time_penalty = category.wrong_answer_time_penalty
        test.max_wrong_answer_allowed = category.max_wrong_answer_allowed
        test.question_time_allowed = category.question_time_allowed
        DBSession.add(test)
        DBSession.flush()
        
        # Get and Randomize Questions
        questionsets = QuestionSets.by({'category_id':self.category_id}).all()
        random.shuffle(questionsets) # randomize first to guarentee all questions
        questionsets = questionsets[0:category.playable_questions] # limit randomized
        
        # Setup Unfinished Questions
        for questionset in questionsets:
            question = self._get_question_variation(questionset, last_test)
            
            result = TestsResults(tests_id=test.id, 
                                  question_sets_id=questionset.id, 
                                  question=question,
                                  answer_choices=TestManager.get_answers(questionset.id)
                                  )
            DBSession.add(result)
            
        
        # okay below
        DBSession.flush()
        user = Users.by({'alias':self.alias}).first()
        user.current_test = test.id
        transaction.commit()

    def _random_question(self,questionset):
        questions = Questions.by({'question_sets_id':questionset.id}).all()
        random.shuffle(questions)
        return questions[0].question
            
    def _get_question_variation(self, questionset, last_test):
        if last_test == None:
            # First test has no past variations so just randomized
            return self._random_question(questionset)
        else:
            # Use next variation and wrap back to beginning when at end
            past_question = TestsResults.by({'tests_id':last_test.id, 'question_sets_id':questionset.id}).first()
            
            questions = Questions.by({'question_sets_id':questionset.id}).all()
            for i, question in enumerate(questions):
                if past_question == None:
                    return self._random_question(questionset)
                if past_question.question == question.question:
                    if (i+1) >= len(questions):
                        return questions[0].question
                    return questions[i+1].question
            
            # purely defensive, should never hit this...
            return self._random_question(questionset)
        
        
        
        
        
        
        
