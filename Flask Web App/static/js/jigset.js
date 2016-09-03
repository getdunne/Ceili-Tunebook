function getTuneOffsets() {
    var elems = document.getElementsByTagName('h2');
    var tops = [];
    for (var i=0; i < elems.length; i++) {
        var rect = elems[i].getBoundingClientRect();
        tops.push(rect.top.toString());
    }
    return tops.join(',');
}
