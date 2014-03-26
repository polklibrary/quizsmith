/*
*   Copyright 2014 UW Board of Regents
*
*   Licensed under the Apache License, Version 2.0 (the "License");
*   you may not use this file except in compliance with the License.
*   You may obtain a copy of the License at
*
*     http://www.apache.org/licenses/LICENSE-2.0
*
*   Unless required by applicable law or agreed to in writing, software
*   distributed under the License is distributed on an "AS IS" BASIS,
*   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
*   See the License for the specific language governing permissions and
*   limitations under the License.
*/

// Thread Reference
var CountDownThread = null;

// Init
jq(document).ready(function(){
    Transitions.setup();
    Playing.start(); // must be last
});

// Selectors for jQuery
Selectors = {
    playing : '#playing',
    countdown : '#countdown',
    transition : '#transition',
    question : '#question',
    answers : '#answers',
    timer : '#timer',
    results : '#results',
    playing_panel : '#playing-panel'
}

// Game Play Class
Playing = {

    transition_in : 'Random',
    transition_out : 'Random',
    delay_before_out : 2,
    category : null,
    count_down_start : 3,
    count_down_size_multiplier : 40,
    question_counter : 0,
    score_counter : 0,
    
    // Start Game
    start : function() {
        //this.category_id = jq.urlParam('category');
        CountDownThread = setInterval(function(){
            jq(Selectors.countdown).html(Playing.count_down_start);
            Playing.count_down_start--;
            var size = parseInt(jq(Selectors.countdown).css('font-size'));
            jq(Selectors.countdown).css('font-size', (size + Playing.count_down_size_multiplier) + 'px');
            
            if(Playing.count_down_start == -1) {
                jq(Selectors.countdown).hide(); 
                clearInterval(CountDownThread);
                CountDownThread = null;
                jq(Selectors.playing_panel).fadeIn(1000);
                Playing.next(); // trigger first question
            }
        },1000);
    },

    
    // Get Next Question
    next : function() {
        var cls = this;
        jq.getJSON(Trivia.current_url() + '/next' + Cache.no_q(), function(data){
            if(!data.finished) {
                cls.category = data.category
                cls.set_question(data.question);
                cls.set_answers(data.answers); 
                Transitions.run(cls.category.transition_in.name, 'in');
                Timer.start(cls.category.question_time_allowed, function(){
                    cls.check();
                });
            }
            else
                Trivia.redirect('/profile/score/' + data.test_id);            
        });
    },

    // Check user selected answer
    check : function(reference) {
        var cls = this;
        var answer = 0;
        if (reference != null)
            answer = jq(reference).prop('data-answer');
            
        jq.getJSON(Trivia.current_url() + '/check?answer=' + answer + '&time=' + Timer.current_time + Cache.no(), function(data){
            Timer.update(data.duration, data.was_correct);
            if (!data.was_correct && reference != null)
                jq(reference).addClass('wrong');
            if (data.was_correct && reference != null)
                jq(reference).addClass('correct');
            if(!data.continue_on) {
                Timer.stop();
                setTimeout(function(){
                    Transitions.run(cls.category.transition_out.name, 'out');
                    cls.results();
                },(cls.delay_before_out*1000));
            }
        });
    },
    
    // Once question is finished, this handles result individual question results
    results : function() {
        var cls = this;
        Timer.reset();
        jq.getJSON(Trivia.current_url() + '/result' + Cache.no_q(), function(data){
        
            cls.score_counter += data.competitive.combined;
            jq(Selectors.playing_panel).fadeIn(500).find('.points').html(cls.score_counter);
            jq(Selectors.playing_panel).fadeIn(500).find('.ranking').html('#' + data.ranking.ranking);
        
            if(data.result.correctly_answered) {
                jq(Selectors.results).find('#status').html( jq('<img>').prop({'src':Trivia.static_url+'/images/correct.png'}) );
                jq(Selectors.results).find('#status').append("Correct");
            }
            else if (!data.result.correctly_answered && data.result.wrong_attempts == cls.category.max_wrong_answer_allowed) {
                jq(Selectors.results).find('#status').html( jq('<img>').prop({'src':Trivia.static_url+'/images/wrong.png'}) );
                jq(Selectors.results).find('#status').append("Wrong");
            }
            else{
                jq(Selectors.results).find('#status').html( jq('<img>').prop({'src':Trivia.static_url+'/images/wrong.png'}) );
                jq(Selectors.results).find('#status').append("No Time Remaining");
            }
            
            jq(Selectors.results).find('#question').html(data.result.question);
            jq(Selectors.results).find('#help').html(data.answer_help);
            jq(Selectors.results).find('#score').html("not calculated");
            jq(Selectors.results).find('#percentage').html(data.percentage + '%');
            jq(Selectors.results).find('#competitive').html(data.competitive.score + ' points with a time bonus of ' + 
                                                            data.competitive.bonus + ' for ' + 
                                                            data.competitive.combined + ' leaderboard points!');
            
            jq(Selectors.results).find('.next, .finish').click(function(){
                jq(Selectors.results).hide();
                jq(Selectors.results).find('.next, .finish').unbind('click');
                Playing.next();
            });
            
            if( cls.total_questions == cls.question_counter) {
                jq(Selectors.results).find('.next').hide();
                jq(Selectors.results).find('.finish').css('display','inline-block');
            }
            
            jq(Selectors.results).fadeIn(1500);
        
        });
        
    },
    
    
    // Setup question on screen
    set_question : function(question) {
        this.question_counter++;
        jq(Selectors.question).html(question);
        jq(Selectors.playing_panel).fadeIn(500).find('.question-counter').html(this.question_counter + ' of ' + this.category.playable_questions);
    },
    
    
    // Setup answers on screen
    set_answers : function(answers) {
        var cls = this;
        jq(Selectors.answers).html('');
        for (var i in answers) {
            var div = jq('<div>').addClass('answer').prop('data-answer',answers[i].id).html(answers[i].content).click(function(){
                jq(this).unbind('click');
                cls.check(jq(this));
            });
            jq(Selectors.answers).append(div);
        }
    }
    
}


// Timer Class with callbacks
Timer = {

    message : 'TIME IS OUT',
    fade_time : 1,
    time_limit : 0,
    current_time : 0,
    time_up_callback : null,
    _clock : null,

    start : function(seconds,callback) {
        var cls = this;
        this.time_limit = seconds + 1;
        this.current_time = seconds + 1;
        this.time_up_callback = callback;
        jq(Selectors.timer).fadeIn(this.fade_time*1000);
    
        cls._clock = setInterval(function(){
            cls.current_time--;
            cls.count_down();
            if(cls.current_time <= 0) {
                cls.time_up_callback();
            }
        },1000);
    },
    
    stop : function() {
        clearInterval(Timer._clock);
        Timer._clock = null;
        this.count_down();
    },
    
    reset : function() {
        jq(Selectors.timer).hide();
        clearInterval(Timer._clock);
        Timer._clock = null;
        jq(Selectors.timer).find('.bar span').remove();
        jq(Selectors.timer).find('.time').html('').removeClass('warn');
    },
    
    update : function(seconds, no_penalty) {
        this.current_time = seconds;
        if(!no_penalty) {
            jq(Selectors.timer).find('.bar').effect('shake',200); 
        }
    },
    
    count_down : function() {
    
        // TIMER BAR
        var width = parseInt(jq(Selectors.timer).find('.bar').width() / this.time_limit) - 5;
        jq(Selectors.timer).find('.bar').html('');
        for(var i = 0; i < this.time_limit; i++) {
            var span = jq('<span>').css({'width':width+'px'});
            if(i >= this.current_time)
                jq(span).addClass('empty');
            else if(this.current_time < 10) {
                jq(span).addClass('warn');
            }
            jq(Selectors.timer).find('.bar').append(span);
        }
        
        // TIMER NUMBER
        if (this.current_time <= 0) {
            jq(Selectors.timer).find('.time').html(this.message);
        }
        else if(this.current_time < 10) {
            jq(Selectors.timer).find('.time').addClass('warn').html(this.current_time).effect('bounce',100); 
        }
        else
            jq(Selectors.timer).find('.time').html(this.current_time);
    },
    
}
