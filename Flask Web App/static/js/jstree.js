// Convert a "book" of the form [name, [children...]] to a jstree dict of the form
// {"text":name, "children":[<converted children>]}
function bookToJstree(book) {
    if (isNaN(book)) {
        var name = book[0];
        var children = book[1];
        var convertedChildren = [];
        for (var i=0; i<children.length; i++) convertedChildren.push(bookToJstree(children[i]));
        return { "text":name, "children":convertedChildren }; 
    }
    else {
        return { "text":book, "icon":"glyphicon glyphicon-list-alt" };
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
    console.log(bookjs);
    var chapters = JSON.parse(bookjs);          // just the chapter list
    console.log(chapters);
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
      "plugins" : [ "wholerow", "dnd" ]
    });
    
    $('#createBtn').on('click', function() {
        var sel = $('#jstree').jstree(true).get_selected()[0];
        var par = $('#jstree').jstree(true).get_parent(sel);
        var success = $('#jstree').jstree(true).create_node(par, 'New', 'last');
        console.log(sel, par, success);
    });

    $('#addSetBtn').on('click', function() {
        var par = $('#jstree').jstree(true).get_selected()[0];
        var node = { 'icon':'glyphicon glyphicon-list-alt', 'text':'1' };
        var success = $('#jstree').jstree(true).create_node(par, node, 'last');
    });

    $('#deleteBtn').on('click', function() {
        var sels = $('#jstree').jstree(true).get_selected();
        $('#jstree').jstree(true).delete_node(sels);
    });

    $('#renameBtn').on('click', function() {
        var sel = $('#jstree').jstree(true).get_selected()[0];
        $('#jstree').jstree(true).edit(sel);
    });
    
    $('#theForm').submit(function() {
        var json = $('#jstree').jstree(true).get_json();
        $('#bookjs').val(JSON.stringify(jstreeToBook({'text':'root', 'children':json})[1]));
        return true;
    });
});
