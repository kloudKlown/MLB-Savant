
// "use strict";
var fs = require('fs');
 
var page = require('webpage').create(),
    system = require('system');
 
if (system.args.length < 2) {
    console.log('Usage: loadurlwithoutcss.js URL');
    phantom.exit();
}
// file = getFilename();
var address = system.args[1];
 
 
page.onResourceRequested = function(requestData, request) {
    if ((/http:\/\/.+?\.css/gi).test(requestData['url']) || requestData.headers['Content-Type'] == 'text/css') {
        console.log('The url of the request is matching. Aborting: ' + requestData['url']);
        request.abort();
    }
};
 
page.open(address, function(status) {
    if (status === 'success') {
        
        function textContent_to_csvFromat(text){
            var final =[];
            var a= "";
            for (var i = 0 ; i < text.length; i=i+1){
                
            
                if (text[i] === "."){
                    a = a.concat(text[i]);
                    a = a.concat(text[i+1]);
                    i = i + 1;
                    if (final.length == 12){
                        final.push(a)
                        return final;
                    }
                    final.push(a);
                    a ="";
                }
                else{
                    a = a.concat(text[i]);
                }
            }
            return final;            
        };

        var player_Name = page.evaluate(function(){
            return document.getElementById('playersCompared').textContent;
        })

        var rh_exit_velocity = page.evaluate(function() {
            var text = document.getElementById('zone_chart_rh_exit_velocity').textContent;
            return text;
        });
        var lh_exit_velocity = page.evaluate(function() {
            var text = document.getElementById('zone_chart_lh_exit_velocity').textContent;
            return text;
        });        

        // console.log(rh_exit_velocity);
        var rightHand =   player_Name.replace(/^\s+|\s+$/gm,'')  +','+ textContent_to_csvFromat(rh_exit_velocity) ; 
        var leftHand =  player_Name.replace(/^\s+|\s+$/gm,'')  +','+  textContent_to_csvFromat(lh_exit_velocity) ;

        // console.log( player_Name.replace(/^\s+|\s+$/gm,'')  +','+ rightHand );
        // console.log( player_Name.replace(/^\s+|\s+$/gm,'')  +','+ leftHand );

        fs.write('players.html' ,rightHand, 'a');

        fs.write('players.html' ,leftHand, 'a');

        phantom.exit();
    } else {
        console.log('Unable to load the address!');
        phantom.exit();
    }
});
