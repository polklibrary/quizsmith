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

Screen = {
	top : function() { return jq(window).scrollTop(); },
	bottom : function() { return jq(window).scrollTop() + jq(window).height(); },
	right : function() { return jq(window).width(); },
	left : function() { return 0; },
}

Transitions = {

    transitions : [],
    add_transition : function(name,in_fn,out_fn) {
        this.transitions.push({'name':name, 'in':in_fn, 'out':out_fn});
    },
    
    run : function(name, type) {
        for (var i in this.transitions) {
            if(this.transitions[i]['name'] == name) 
                this.transitions[i][type.toLowerCase()].call();
        }
    },
    
    reset : function() {
        jq(Selectors.transition).removeAttr('style'); 
    },
    
    setup : function() {
        var cls = this;
        
        // === START Random ============================
        var random_in = function() {
            var i = Math.floor(Math.random() * ((cls.transitions.length - 1) - 0) + 0); 
            cls.transitions[i]['in'].call();
        }
        var random_out = function() {
            var i = Math.floor(Math.random() * ((cls.transitions.length - 1) - 0) + 0); 
            cls.transitions[i]['out'].call();
        }
        this.add_transition('Random', random_in, random_out);
        // === END Random ============================
        
        // === START Slide Right ============================
        var slide_in_right = function() {
            var move = 10000;
            jq('body').css({'overflow-x':'hidden'});
            jq(Selectors.transition).css({'margin-left':(-move)+'px','display':'block'});
            jq(Selectors.transition).animate({'margin-left': '+=' + move}, 1000);
        }
        var slide_out_right = function() {
            var move = 10000;
            jq(Selectors.transition).css({'position':'fixed'});
            jq(Selectors.transition).animate({'margin-left': '+=' + move}, {
                duration: 1000,
                complete: function() {
                    jq('body').css({'overflow-x':'auto'});
                    cls.reset();
                }
            });
        }
        this.add_transition('Slide Right', slide_in_right, slide_out_right);
        // === END Slide Right ============================
        
        // === START Slide Left ============================
        var slide_in_left = function() {
            var move = 10000;
            jq('body').css({'overflow-x':'hidden'});
            jq(Selectors.transition).css({'margin-left':(move)+'px','display':'block'});
            jq(Selectors.transition).animate({'margin-left': '-=' + move}, 1000);
        }
        var slide_out_left = function() {
            var move = 10000;
            jq(Selectors.transition).css({'position':'fixed'});
            jq(Selectors.transition).animate({'margin-left': '-=' + move}, {
                duration: 1000,
                complete: function() {
                    jq('body').css({'overflow-x':'auto'});
                    cls.reset();
                }
            });
        }
        this.add_transition('Slide Left', slide_in_left, slide_out_left);
        // === END Slide Left ============================
        
        // === START Slide Up ============================
        var slide_in_up = function() {
            var move = 10000;
            jq('body').css({'overflow-y':'hidden'});
            jq(Selectors.transition).css({'margin-top':(move)+'px','display':'block'});
            jq(Selectors.transition).animate({'margin-top': '-=' + move}, 1000);
        }
        var slide_out_up = function() {
            var move = 10000;
            jq(Selectors.transition).css({'position':'fixed'});
            jq(Selectors.transition).animate({'margin-top': '-=' + move}, {
                duration: 1000,
                complete: function() {
                    jq('body').css({'overflow-y':'auto'});
                    cls.reset();
                }
            });
        }
        this.add_transition('Slide Up', slide_in_up, slide_out_up);
        // === END Slide Up ============================
        
        // === START Slide Down ============================
        var slide_in_down = function() {
            var move = 10000;
            jq('body').css({'overflow-y':'hidden'});
            jq(Selectors.transition).css({'margin-top':(-move)+'px','display':'block'});
            jq(Selectors.transition).animate({'margin-top': '+=' + move}, 1000);
        }
        var slide_out_down = function() {
            var move = 10000;
            jq(Selectors.transition).css({'position':'fixed'});
            jq(Selectors.transition).animate({'margin-top': '+=' + move}, {
                duration: 1000,
                complete: function() {
                    jq('body').css({'overflow-y':'auto'});
                    cls.reset();
                }
            });
        }
        this.add_transition('Slide Down', slide_in_down, slide_out_down);
        // === END Slide Down ============================
        
        // === START Fade ============================
        var fade_in = function() {
            jq(Selectors.transition).fadeIn(1000);
        }
        var fade_out = function() {
            jq(Selectors.transition).css({'position':'fixed'});
            jq(Selectors.transition).fadeOut(1000, function() {
                cls.reset();
            });
        }
        this.add_transition('Fade In|Out', fade_in, fade_out);
        // === END Fade ============================
        
        // === START Implode|Explode ============================
        var implode = function() {
            jq(Selectors.transition).css({'width':jq(Selectors.playing).width()});
            jq(Selectors.transition).addClass('implode');
            jq(Selectors.transition).show('explode', {'pieces':90}, 750, function() {
                jq(Selectors.transition).removeClass('implode');
            });
        }
        var explode = function() {
            jq(Selectors.transition).css({'width':jq(Selectors.playing).width()});
            jq(Selectors.transition).addClass('explode');
            jq(Selectors.transition).effect('explode', {'pieces':90}, 750, function() {
                jq(Selectors.transition).removeClass('explode');
                cls.reset();
            });
        }
        this.add_transition('Implode|Explode', implode, explode);
        // === END Implode|Explode ============================
        
        // === START Blinds ============================
        var blind_in = function() {
            jq(Selectors.transition).css({'position':'fixed'});
            jq(Selectors.transition).show('blind', 500, function() {
            });
        }
        var blind_out = function() {
            jq(Selectors.transition).css({'position':'fixed'});
            jq(Selectors.transition).effect('blind', 500, function() {
                cls.reset();
            });
        }
        this.add_transition('Blinds', blind_in, blind_out);
        // === END Blinds ============================
        
        // === START Implode|Explode ============================
        var inflate = function() {
            jq(Selectors.transition).css({'width':jq(Selectors.playing).width()});
            jq(Selectors.transition).addClass('inflate');
            jq(Selectors.transition).show('puff', {'percent':200}, 750, function() {
                jq(Selectors.transition).removeClass('inflate');
            });
        }
        var deflate = function() {
            jq(Selectors.transition).css({'width':jq(Selectors.playing).width()});
            jq(Selectors.transition).addClass('deflate');
            jq(Selectors.transition).effect('puff', {'percent':200}, 750, function() {
                jq(Selectors.transition).removeClass('deflate');
                cls.reset();
            });
        }
        this.add_transition('Inflate|Deflate', inflate, deflate);
        // === END Implode|Explode ============================

    },

}