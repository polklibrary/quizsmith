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
var jq = $.noConflict();
jq.urlParam = function(name) {
    var results = new RegExp('[\\?&]' + name + '=([^&#]*)').exec(window.location.href);
    if (!results) { return 0; }
    return decodeURIComponent(results[1]) || 0;
}

// Init
jq(document).ready(function(){
    Trivia.init();
});

// Trivia Setup and Utilities
Trivia = {

    root_url : '', // Note: The url is set in the master.pt
    static_url : '', // Note: The url is set in the master.pt

    init : function() {
        var cls = this;
        jq('input[name="to.menu"], .to_menu').click(function() {
            cls.redirect();
        }); 
        jq('.tooltip').tooltip({ position: { my: "left+15 center", at: "right center" } });
    },

    current_url : function() {
        return window.location.href;
    },
    
    redirect : function(where) {
        if(where == null) where = '';
        window.location.href = this.root_url + where;
    },
    
}

// Cachekey generator, prevents IE from caching
Cache = {
    no : function() {
        return '&no.cache' + new Date().getTime();
    },
    no_q : function() {
        return '?no.cache' + new Date().getTime();
    }
}

