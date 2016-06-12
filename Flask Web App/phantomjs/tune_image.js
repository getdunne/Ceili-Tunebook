"use strict";

var system = require('system');
var args = system.args;

var page = require('webpage').create();
page.viewportSize = { width: 1600, height : 2400 };
page.zoomFactor = 2.0
page.open('http://127.0.0.1:5000/tune_img/' + args[1], function() {
    document.body.bgColor = 'white';
    page.render('temp.png');
    phantom.exit();
});
