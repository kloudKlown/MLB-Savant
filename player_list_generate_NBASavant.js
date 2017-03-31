// Render Multiple URLs to file
 
"use strict";
var RenderUrlsToFile, arrayOfUrls, system;
 
system = require("system");
var fs = require('fs');
 
/*
Render given urls
@param array of URLs to render
@param callbackPerUrl Function called after finishing each URL, including the last URL
@param callbackFinal Function called after finishing everything
*/
RenderUrlsToFile = function(urls, callbackPerUrl, callbackFinal) {
    var getFilename, next, page, retrieve, urlIndex, webpage;
    urlIndex = 0;
    webpage = require("webpage");
    page = null;
    getFilename = function() {
        return "rendermulti-" + urlIndex + ".png";
    };
    next = function(status, url, file) {
        page.close();
        callbackPerUrl(status, url, file);
        return retrieve();
    };
    retrieve = function() {
        var url;
        if (urls.length > 0) {
            url = urls.shift();
            urlIndex++;
            page = webpage.create();
            page.viewportSize = {
                width: 800,
                height: 600
            };
            page.settings.userAgent = "Phantom.js bot";
 
            return page.open("http://" + url, function(status) {
                var file;
                file = getFilename();
                if (status === "success") {
                     
                    return window.setTimeout((function() {
                        page.render(file);
                        fs.write( file+'test.html', page.content, 'w');
                        return next(status, url, file);
                    }), 2000);
                } else {
                    return next(status, url, file);
                }
            });
        } else {
            return callbackFinal();
        }
    };
    return retrieve();
};
 
arrayOfUrls = null;
 
if (system.args.length > 1) {
    arrayOfUrls = Array.prototype.slice.call(system.args, 1);
} else {
    console.log("Usage: phantomjs render_multi_url.js [domain.name1, domain.name2, ...]");
    //hitters
    // arrayOfUrls = ["mlb.mlb.com/stats/sortable.jsp#elem=%5Bobject+Object%5D&tab_level=child&click_text=Sortable+Player+hitting&game_type='R'&season=2016&season_type=ANY&league_code='MLB'&sectionType=sp&statType=hitting&page=1&timeframe=d7&split=&last_x_days=7",
    // "mlb.mlb.com/stats/sortable.jsp#elem=%5Bobject+Object%5D&tab_level=child&click_text=Sortable+Player+hitting&game_type='R'&season=2016&season_type=ANY&league_code='MLB'&sectionType=sp&statType=hitting&page=2&timeframe=d7&split=&last_x_days=7",
    // "mlb.mlb.com/stats/sortable.jsp#elem=%5Bobject+Object%5D&tab_level=child&click_text=Sortable+Player+hitting&game_type='R'&season=2016&season_type=ANY&league_code='MLB'&sectionType=sp&statType=hitting&page=3&timeframe=d7&split=&last_x_days=7",
    // "mlb.mlb.com/stats/sortable.jsp#elem=%5Bobject+Object%5D&tab_level=child&click_text=Sortable+Player+hitting&game_type='R'&season=2016&season_type=ANY&league_code='MLB'&sectionType=sp&statType=hitting&page=4&timeframe=d7&split=&last_x_days=7"];
 
    //pitchers
    arrayOfUrls = ["mlb.mlb.com/stats/sortable.jsp#elem=%5Bobject+Object%5D&tab_level=child&click_text=Sortable+Player+pitching&game_type='R'&season=2016&season_type=ANY&league_code='MLB'&sectionType=sp&statType=pitching&page=1&timeframe=d30&split=&last_x_days=30",
    "mlb.mlb.com/stats/sortable.jsp#elem=%5Bobject+Object%5D&tab_level=child&click_text=Sortable+Player+pitching&game_type='R'&season=2016&season_type=ANY&league_code='MLB'&sectionType=sp&statType=pitching&page=2&timeframe=d30&split=&last_x_days=30",
    "mlb.mlb.com/stats/sortable.jsp#elem=%5Bobject+Object%5D&tab_level=child&click_text=Sortable+Player+pitching&game_type='R'&season=2016&season_type=ANY&league_code='MLB'&sectionType=sp&statType=pitching&page=3&timeframe=d30&split=&last_x_days=30",
    "mlb.mlb.com/stats/sortable.jsp#elem=%5Bobject+Object%5D&tab_level=child&click_text=Sortable+Player+pitching&game_type='R'&season=2016&season_type=ANY&league_code='MLB'&sectionType=sp&statType=pitching&page=4&timeframe=d30&split=&last_x_days=30"];
}
 
RenderUrlsToFile(arrayOfUrls, (function(status, url, file) {
    if (status !== "success") {
        return console.log("Unable to render '" + url + "'");
    } else {
 
        return console.log("Rendered '" + url + "' at '" + file + "'");
 
    }
}), function() {
    return phantom.exit();
});