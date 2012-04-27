function svg_load(element_id, callback) {
    // function that sets up an onload event handler on an embeded svg object
    // and runs a callback function onload, passing in the svg document root
    var a = document.getElementById(element_id);
    a.addEventListener("load", function() {
        var svg = a.getSVGDocument();
        var svgRoot = svg.documentElement;
        
        callback(svgRoot);
        scorecard_front(svgRoot);
    });
}
function scorecard_front(docroot) {
    var country_name = $("#_countryname_1_", docroot);
    country_name.text("South Africa");
}
