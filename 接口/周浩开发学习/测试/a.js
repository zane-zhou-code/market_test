document.getElementById('i1').innerText
function func() {

}
document.getElementsByTagName('div')
document.getElementsByName('')
document.getElementsByClassName('')
(function(){function h(a){return{get:function(b){var c=JSON.parse(a.getItem(b));return!c||Date.parse(c.expires)<=(new Date).getTime()?(a.removeItem(b),null):c.value},set:function(b,c,m){c={value:c,expires:m.toUTCString()};a.setItem(b,JSON.stringify(c))},remove:function(b){a.removeItem(b)}}}function d(a,b,c,m,d){this.parseCommand=function(e,g){function h(){var a=JSON.stringify({messageId:k,value:n||!1});window.parent.postMessage(a,"*")}var p=s[a],q=e.action,r=e.key,k=e.messageId,f=e.siteId,f=m?r:r+
":"+f,n=e.value,l=e.expiresMinutes||1440*(e.expiresDays||365),t=function(){var a=new Date;a.setTime(a.getTime()+6E4*l);return a}();if(!function(){var a={_hjSet:c,_hjGet:b,_hjRemove:c}[q]||[];return 0<=a.indexOf("*")||0<=a.indexOf(g)}())throw Error("Command "+q+" not allowed on key: "+r);switch(q){case "_hjSet":p.set(f,n,t,d);break;case "_hjGet":n=p.get(f);h();break;case "_hjRemove":p.remove(f)}}}function k(a){try{var b=JSON.parse(a.data);b.key&&l[b.key]&&l[b.key].parseCommand(b,a.origin)}catch(c){return null}}
var s;try{var g;try{g=localStorage}catch(u){g=sessionStorage}s={cookie:{get:function(a){return(a=RegExp("(?:^|; )"+a+"=([^;]*)").exec(document.cookie))?a[1]:void 0},set:function(a,b,c,d){a=[a+"="+b,"path=/","expires="+c.toUTCString()].concat(d||[]).join("; ");document.cookie=a},remove:function(a){document.cookie=a+"=; expires=Tue, 13 Mar 1979 00:00:00 UTC; path=/;"}},localStorage:h(g),sessionStorage:h(sessionStorage)}}catch(v){return}var l={_hjOptOut:new d("cookie",["*"],["https://www.hotjar.com",
"https://local.hotjar.com","http://local.hotjar.com","https://insights-staging.hotjar.com","http://insights-staging.hotjar.com"],!0,["SameSite=None","Secure"]),grant_consent:new d("cookie",["*"],["*"],!1),screenshot_retake:new d("localStorage",["*"],["*"],!1),screenshot_active_retake:new d("sessionStorage",["*"],["*"],!1)};window.addEventListener?window.addEventListener("message",k,!1):window.attachEvent("onmessage",k)})();
