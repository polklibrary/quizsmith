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


// Simple confirmation validator class
Validators = {
    
    run : function() {
        setInterval(function(){
            jq('.validate').each(function(i,t) {
                if(jq(t).attr('data-validate-on') != 'true') {
                    console.log("attaching");
                    Validators.confirms(t, jq(t).attr('data-validate-msg'));
                    jq(t).attr('data-validate-on','true');
                }
            });
        },100); 
    },

    confirms : function(reference,msg) {
        if (msg == null || typeof msg == 'undefined')
            msg = 'Are you sure you want to remove this?';
        jq(reference).click(function(e) {
            var r = confirm(msg);
            if (r==false) {
                Validators._queued = null;
                return false;
            }
            else {
                var fn = jq(reference).attr('data-validate-fn');
                if (typeof fn != 'undefined' || fn != null)
                    window[fn](reference,e);
                return true;
            }
        });
    }

}


jq(document).ready(function(){

    Validators.run();

    jq('#nav-links > a:not(.nav-x)').each(function(i,t){
        if (document.location.href.indexOf(jq(t).attr('href')) != -1)
            jq(t).addClass('nav-selected');
    });
    
    if (jq('#message').is(":visible")) {
        jq('#message').effect("highlight", {'color':'#FFFF00', 'easing':'easeInOutQuint'}, 500, function(){
            jq('#message').effect("highlight", {'color':'#FFFF00', 'easing':'easeInOutQuint'}, 500, function(){
                jq('#message').fadeOut(7500);
            });
        });
    }
        
});

