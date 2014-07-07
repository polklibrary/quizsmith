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

// TinyMCE Settings
tinyMCE.init({
    theme_advanced_disable : 'styleselect,justifyfull,hr,help,charmap',
    theme_advanced_buttons1 : 'bold,italic,underline,strikethrough,justifyleft,justifycenter,justifyright,formatselect,bullist,numlist,outdent,indent,undo,redo,link,unlick,anchor,image,cleanup,code',
    valid_elements : 'a[href|name|target],strong/b,em/i,p[style],br,img[src|alt|width|height],pre,ul,ol,li,address,h1,h2,h3,h4,h5,h6,span[!style],iframe[src|width|height|frameBorder]',
    valid_styles : { '*' : 'font-weight,text-decoration,text-align,padding,padding-top,padding-bottom,padding-left,padding-right,border,vertical-align,margin,margin-bottom,margin-top,margin-left,margin-right,border,width,height'},
});