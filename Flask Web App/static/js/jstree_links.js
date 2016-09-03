// Convert a "book" of the form [name, [children...]] to a jstree dict of the form
// {"text":name, "children":[<converted children>]}
function bookToJstree(book) {
    if (isNaN(book[0])) {
        var name = book[0];
        var children = book[1];
        var convertedChildren = [];
        for (var i=0; i<children.length; i++) convertedChildren.push(bookToJstree(children[i]));
        return { "text":name, "children":convertedChildren }; 
    }
    else {
        return { "text":book[1], "icon":"glyphicon glyphicon-list-alt", "a_attr":{ "href": "/showset/" + book[0] } };
    }
}

// Convert a jstree back to book form
function jstreeToBook(tree) {
    if ("icon" in tree && tree["icon"] != true) {
        var setID = parseInt(tree["text"]);
        return setID;
    }
    else {
        var name = tree["text"];
        var children = tree["children"];
        var convertedChildren = [];
        for (var i=0; i<children.length; i++) convertedChildren.push(jstreeToBook(children[i]));
        return [name, convertedChildren];
    }
}

$(function () {
    var bookjs = $('#bookjs').val();
    var chapters = JSON.parse(bookjs);          // just the chapter list
    if (chapters.length == 0) chapters = [ ['First Heading', []] ];
    var book = ['root', chapters];    // make into a true book with dummy heading
    var tree = bookToJstree(book);
    var booktitle = $('#booktitle').val();
    
    $('#jstree').jstree({
      "core" : {
        "themes" : { "variant" : "large" },
        'data' : tree['children'],
        "check_callback": true
      },
      "plugins" : [ "wholerow" ]
    }).bind("select_node.jstree", function (e, data) {
     var href = data.node.a_attr.href;
     document.location.href = href;
    });
});
