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

    //if (document.location.href.indexOf('localhost') == -1) {
    if (document.location.href.indexOf('uwosh.edu/library/anvil/game') == -1) { 
        jq('body').addClass('duck');
        Playing.sound_effect_on = true;
    }
    
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

    sound_effect_on : false,
    transition_in : 'Random',
    transition_out : 'Random',
    delay_before_out : 2,
    category : null,
    count_down_start : 5,
    count_down_size_multiplier : 40,
    question_counter : 0,
    total_questions : 0,
    score_counter : 0,
    penalty : 15,
    wrong : 0,
    max_wrong : 0,
    their_answers : [],
    
    // Start Game
    start : function() {
        //this.category_id = jq.urlParam('category');
        CountDownThread = setInterval(function(){
            jq(Selectors.countdown).html(Playing.count_down_start);
            Playing.count_down_start--;
            var size = parseInt(jq(Selectors.countdown).css('font-size'));
            jq(Selectors.countdown).css('font-size', (size + Playing.count_down_size_multiplier) + 'px');
            
            if(Playing.count_down_start == -1) {
                jq(Selectors.countdown).fadeOut(300,function(){
                    clearInterval(CountDownThread);
                    CountDownThread = null;
                    Playing.next(); // trigger first question
                }); 
            }
        },1000);
    },

    // Get Next Question
    next : function() {
        var cls = this;
        jq.getJSON(Trivia.current_url() + '/next' + Cache.no_q(), function(data){
            if(!data.finished) {
                cls.category = data.category;
                cls.set_question(data.question);
                cls.set_answers(data.answers);
                cls.total_questions = data.category.playable_questions;
                cls.penalty = data.category.wrong_answer_time_penalty;
                cls.wrong = 0;
                cls.max_wrong = data.category.max_wrong_answer_allowed;
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
            if (!data.was_correct && reference != null) {
                jq(reference).addClass('wrong');
                cls.wrong += 1;
                cls.mark_answer(answer,-1);
            }
            if (data.was_correct && reference != null) {
                jq(reference).addClass('correct');
                cls.mark_answer(answer,1);
                cls.halt();
            }
            if(!data.continue_on) {
                cls.halt();
                if (cls.wrong == cls.max_wrong) 
                    Timer.finish_animate();
                else
                    Timer.stop();
                setTimeout(function(){
                    Transitions.run(cls.category.transition_out.name, 'out');
                    //cls.results(); moved to transitions
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
                jq(Selectors.results).find('#status').html( jq('<img>').prop({'src':Trivia.static_url+'/images/correct-stamp.png'}) );
            }
            else if (!data.result.correctly_answered && data.result.wrong_attempts == cls.category.max_wrong_answer_allowed) {
                jq(Selectors.results).find('#status').html( jq('<img>').prop({'src':Trivia.static_url+'/images/wrong-stamp.png'}) );
            }
            else {
                jq(Selectors.results).find('#status').html( jq('<img>').prop({'src':Trivia.static_url+'/images/wrong-nt-stamp.png'}) );
            }
            
            jq(Selectors.results).find('#question').html(data.result.question);
            
            jq(Selectors.results).find('#answers').html('');
            for(var i in cls.their_answers) {
                classname = '';
                if (cls.their_answers[i].answered == -1)
                    classname = 'wrong';
                else if (cls.their_answers[i].answered == 1)
                    classname = 'correct';
                var div = jq('<div>').addClass(classname).html(cls.their_answers[i].content);
                jq(Selectors.results).find('#answers').append(div);
            }
            
            jq(Selectors.results).find('#tip').html(data.answer_help);
            jq(Selectors.results).find('#score').html("not calculated");
            jq(Selectors.results).find('#percentage').html(data.percentage + '%');
            jq(Selectors.results).find('#competitive').html(data.competitive.score + ' points with a time bonus of ' + 
                                                            data.competitive.bonus + ' for ' + 
                                                            data.competitive.combined + ' leaderboard points!');
            
            jq(Selectors.results).find('.next, .finish').click(function(){
                jq(Selectors.results).stop(true,true).hide();
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
    
    halt : function() {
        jq('div.answer').unbind('click');
    },
    
    mark_answer : function(answer_id, answered) {
        for (var i in this.their_answers)
            if (this.their_answers[i].id == answer_id)
                this.their_answers[i].answered = answered;
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
        cls.their_answers = [];
        jq(Selectors.answers).html('');
        for (var i in answers) {
            cls.their_answers.push({'id':answers[i].id,'answered':0,'content':answers[i].content});
            var div = jq('<div>').addClass('answer').prop('data-answer',answers[i].id).html(answers[i].content).click(function(){
                jq(this).unbind('click');
                cls.check(jq(this));
            });
            jq(Selectors.answers).append(div);
        }
    },
    
    play_sound : function() {
        try {
            if (this.sound_effect_on)
                document.getElementById('soundeffect').play();
        }catch(e){
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
    _past_distance : 100,

    start : function(seconds, callback) {
        var cls = this;
        this.time_limit = seconds + 1;
        this.current_time = seconds + 1;
        this.time_up_callback = callback;
        //jq(Selectors.timer).fadeIn(this.fade_time*1000);
        this.animate();
        this._chain_animate(true);
        cls._clock = setInterval(function(){
            cls.current_time--;
            cls.count_down();
            if(cls.current_time <= 0) {
                cls.time_up_callback();
            }
        },1000);
    },
    
    stop : function() {
        if(this.current_time > 0)
            jq(Selectors.timer).find('.falling-item').stop();
        clearInterval(Timer._clock);
        Timer._clock = null;
        this.count_down();
    },
    
    reset : function() {
        clearInterval(Timer._clock);
        Timer._clock = null;
        Timer. _past_distance = 100;
        jq(Selectors.timer).find('.falling-item').stop(true,true).removeClass('warn early-warn').html('').css({'top':'0px'});
        jq(Selectors.timer).find('.base').removeClass('worried ouch');
        jq(Selectors.timer).find('.falling-zone').removeClass('thoughts');
        this._chain_animate(false);
    },
   
    update : function(seconds, no_penalty) {
        var cls = this;
        this.current_time = seconds;
        
        if (!no_penalty && this.current_time > 0) {
            // This is the shake.
            // Native jQuery shake causes background to become invisible, this doesn't
            jq(Selectors.timer).find('.falling-item').animate({
                'left':'+=10px'
            },50, function(){
                jq(Selectors.timer).find('.falling-item').animate({
                    'left':'-=20px'
                },50, function() {
                    jq(Selectors.timer).find('.falling-item').animate({
                        'left':'+=10px'
                    },50);
                });
            });
        }
        
        if (this.current_time <= 1) {
            jq(Selectors.timer).find('.falling-item').stop(true,true).animate({
                'top':'+='+cls._distance().bottom+'px'
            }, 100,'linear');
        }

    },
    
    finish_animate : function() {
        var cls = this;
        jq(Selectors.timer).find('.falling-item').stop(true,true).animate({
            'top':'+='+cls._distance().bottom+'px'
        }, 100,'linear', function(){
            Playing.play_sound();
            cls.stop();
        });
    },
    
    count_down : function() {
    
        // Set Current Time
        jq(Selectors.timer).find('.falling-item').html('&nbsp;' + this.current_time);
        
        // Switch element Anvil hits...
        if (this.current_time <= 0) {
            Playing.play_sound();
            jq(Selectors.timer).find('.base').addClass('ouch');
            jq(Selectors.timer).find('.falling-zone').removeClass('thoughts');
            jq(Selectors.timer).find('.falling-item').addClass('warn');
            jq(Selectors.timer).find('.base').removeClass('worried');
        }
        else if (this.current_time <= (this.time_limit/3)) {
            jq(Selectors.timer).find('.falling-zone').addClass('thoughts');
            jq(Selectors.timer).find('.falling-item').addClass('warn');
        }
        else if (this.current_time <= (this.time_limit/1.5)) {
            jq(Selectors.timer).find('.base').addClass('worried');
            jq(Selectors.timer).find('.falling-item').addClass('early-warn');
        }
        
    },
    
   
    _distance : function() {
        var zone_top = jq(Selectors.timer).find('.falling-zone').position().top;
        var obj_top = jq(Selectors.timer).find('.falling-item').position().top;
        var zone_y_passed = obj_top - zone_top;
        
        var zone_height = jq(Selectors.timer).find('.falling-zone').height() - zone_y_passed;
        var obj_height = jq(Selectors.timer).find('.falling-item').height();
        
        bottom = zone_height-obj_height
        y = (bottom / this.current_time);
        
        penalty = false;
        if (this._past_distance+1 <= y) // +2 padding
            penalty = true;
            
        tmp = y;
        if (penalty)
            y = this._past_distance * Playing.penalty;
        this._past_distance = tmp;
                
        return {'update':y , 'bottom':bottom};
    },    
    
    animate : function () {
        var cls = this;
        if(this.current_time > 0) {
            jq(Selectors.timer).find('.falling-item').animate({
                'top':'+='+cls._distance().update+'px'
            }, 1000,'linear', function(){
                jq(Selectors.timer).find('.falling-item').stop(true,true); // purge any animation
                cls.animate();
            });
        }
    },

    _chain_animate : function(val) {
        if(val)
            jq(Selectors.timer).find('#chain').prop('src', Trivia.static_url + '/images/chain-swing-action.gif');
        else
            jq(Selectors.timer).find('#chain').prop('src', Trivia.static_url + '/images/chain-swing-static.gif');
    }

    
}
