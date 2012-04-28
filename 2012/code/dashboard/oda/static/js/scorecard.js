function svg_load(element_id, callback, params) {
    console.log("Setting up onload event handler on " + element_id);
    /*
    function that sets up an onload event handler on an embeded svg object
    and runs a callback function onload, passing in the svg document root
    
    element_id - element to set an onload event handler on
    callback - function to call on load
    params - parameters to pass to callback function
    */
   
    var a = document.getElementById(element_id);
    a.addEventListener("load", function() {
        console.log(element_id + " has loaded");
        console.log("Callback: " + callback);
        console.log("Params: " + params);
        var svg = a.getSVGDocument();
        var svgRoot = svg.documentElement;
        
        callback(svgRoot, params);
    });
}

function ScorecardFrontPage(docroot, iso3) {
    this.docroot = docroot;
    this.iso3 = iso3;
}

ScorecardFrontPage.prototype.setup_country_name = function() {
    var ds = new Miso.Dataset({
        url : "/oda/data/country_name/" + this.iso3 + "/"
    });

    var docroot = this.docroot
    ds.fetch({
        success: function() {
            console.log('Country name dataset loaded');
            console.log(this.column("Name").data);
            var country_name = $("#_countryname_1_", docroot);
            country_name.text(this.column("Name").data[0]);
        }
    });
};

ScorecardFrontPage.prototype.setup_indicator_block = function() {
    var ds = new Miso.Dataset({
        url : "/oda/data/" + this.iso3 + "/"
    });

    ds.fetch({
        success: function() {
            console.log('Indicator dataset loaded');
            data2000 = this.where({
                rows : function(row) {
                    return row.year == "2000";
                }
            });
            console.log("2000 mean", data2000.mean("value"));
        }
    });
};

ScorecardFrontPage.prototype.generate_scorecord = function() {
    this.setup_country_name();
    this.setup_indicator_block();
};


function scorecard_back(docroot) {
    alert('back');
}
