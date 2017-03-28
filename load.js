
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
        
        fs.write('players.html' , page.content, 'w');
        phantom.exit();
    } else {
        console.log('Unable to load the address!');
        phantom.exit();
    }
});
