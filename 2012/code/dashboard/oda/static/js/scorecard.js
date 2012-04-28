// Add a startWith method to strings
if (typeof String.prototype.startsWith != 'function') {
  String.prototype.startsWith = function (str){
    return this.indexOf(str) == 0;
  };
}
/*
Miso.types.in_millions = {
    name : "in_millions",
    test : function(v) { return true; },
    compare : function(v1, v2) { return v1 - v2; },
    numeric : function(v) { return v / 1000000;},
    coerce : function(v) {
        if (_.isNull(v)) { return null; }
        return _.isNaN(v) ? null : +v;
    }
};
*/
var WHO = {};

/*
// A parser that converts rows to columns
WHO.ReshapeParser = function(options) {
    if (typeof options.reshape_options == "undefined") {
          throw "Expected reshape_options parameter to be set"
    }
    this.reshape_key = options.reshape_options.reshape_key;
    this.reshape_value = options.reshape_options.reshape_value;
};

_.extend(
    WHO.ReshapeParser.prototype, 
    Miso.Parsers.prototype,
    {
        parse : function(data) {
            var cols = {}
            var reshape_key = this.reshape_key;
            var reshape_value = this.reshape_value;
            var dataYears = {}

            _.each(data, function(d) {
                if (_.indexOf(dataColumns, d.year) < 0) {
                    dataYears[d.year] = {}
                }
                var currentDataYear = dataYears[d.year];
                currentDataYear[d[reshape_key]] = d[reshape_value]
            });
            
            return {
                columns: ._keys(cols),
                data : dataColumns
            };
        }
    }
);
*/


// A parser that reformats the WHO indicator data from rows to columns
WHO.IndicatorsParser = function(options) {};
_.extend(
    WHO.IndicatorsParser.prototype, Miso.Parsers.prototype,
    {
        parse : function(data) {
            var columns = [
                "population", 
                "total_commitments", "total_disbursements", 
                "health_commitments", "health_disbursements", 
                "ratio_commitments", "ratio_disbursements", 
                "commitments_per_capita", "disbursements_per_capita", 
                "regional_avg_commitements", "regional_avg_disbursements", 
                "external_resources", 
                "gghe_perc", "gghe_cap"
            ],
            dataColumns = {
                population : [], 
                total_commitments : [], 
                total_disbursements : [], 
                health_commitments : [], 
                health_disbursements : [], 
                //ratio_commitments : [], 
                //ratio_disbursements : [], 
                commitments_per_capita : [], 
                disbursements_per_capita : [], 
                //regional_avg_commitements : [], 
                //regional_avg_disbursements : [], 
                external_resources : [], 
                gghe_perc : [], 
                gghe_cap : [],
                gghe_cap_ppp : [],
                year : []
            }

            data.sort(function(a, b) {
                if (a.year < b.year) return -1;
                if (a.year > b.year) return 1;
                return 0;
            });

            var indicator_map = {
                1 : "gghe_perc",
                2 : "gghe_cap",
                3 : "gghe_cap_ppp",
                4 : "external_resources",
                5 : "health_commitments",
                6 : "health_disbursements",
                7 : "population",
                8 : "commitments_per_capita",
                9 : "disbursements_per_capita",
                10 : "total_commitments",
                11 : "total_disbursements"
            }
            years = {}
            _.each(data, function(c) {
                var column = dataColumns[indicator_map[c.indicator]];
                column.push(c.value);
                years[c.year] = c.year;
            });
            dataColumns["year"] = _.keys(years).sort();

            return {
                columns: columns,
                data : dataColumns
            };
        }
    }
);

// A parser that reformats the WHO indicator data from rows to columns
WHO.AllocationsParser = function(options) {};
_.extend(
    WHO.AllocationsParser.prototype, Miso.Parsers.prototype,
    {
        parse : function(data) {
            var columns = [
                "year", 
                "c_hpam", "c_mdg6", "c_ohp", "c_rhfp", "c_total",
                "d_hpam", "d_mdg6", "d_ohp", "d_rhfp", "d_total"
            ],
            dataColumns = {
                year : [], 
                c_hpam : [], c_mdg6 : [], c_ohp : [], c_rhfp : [], 
                d_hpam : [], d_mdg6 : [], d_ohp : [], d_rhfp : []
            }

            data.sort(function(a, b) {
                if (a.year < b.year) return -1;
                if (a.year > b.year) return 1;
                return 0;
            });

            var indicator_map = {
                1 : "hpam",
                2 : "mdg6",
                3 : "ohp",
                4 : "rhfp"
            }
            years = {}
            _.each(data, function(c) {
                
                var c_column = dataColumns["c_" + indicator_map[c.mdgpurpose]];
                var d_column = dataColumns["d_" + indicator_map[c.mdgpurpose]];
                c_column.push(c.commitment);
                d_column.push(c.disbursement);
                years[c.year] = c.year;
            });

            dataColumns["year"] = _.keys(years).sort();

            return {
                columns: columns,
                data : dataColumns
            };
        }
    }
);

function ScorecardFrontPage(docroot, iso3) {
    this.docroot = docroot;
    this.iso3 = iso3;
    this.all_years = [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010];
}

ScorecardFrontPage.prototype.setup_country_name = function() {
    var ds = new Miso.Dataset({
        url : "/oda/data/country_name/" + this.iso3 + "/"
    });

    var docroot = this.docroot
    ds.fetch({
        success: function() {
            console.log('Country name dataset loaded');
            console.log(ds.column("Name"));
            console.log(this.column("Name").data);
            var country_name = d3.select("#_countryname_1_");
            country_name.text(this.column("Name").data[0]);
        }
    });
};

ScorecardFrontPage.prototype.setup_indicator_block = function() {
    var ds = new Miso.Dataset({
        url : "/oda/data/" + this.iso3 + "/",
        parser : WHO.IndicatorsParser,
        /*
        parser : WHO.ReshapeParser,
        reshape_options : {
            reshape_key : "indicator",
            reshape_value : "value"
        },
        */
        columns : [
            { name : "gghe_perc", type : "string", before : function(v) {
                return sprintf("%.1f%%", v * 100);
            }},
            { name : "gghe_cap", type : "number", before : function(v) {
                return sprintf("%.1f", v);
            }},
            { name : "gghe_cap_ppp", type : "number" },
            { name : "external_resources", type : "string", before : function(v) {
                return sprintf("%.1f%%", v * 100);
            }},
            { name : "health_commitments", type : "number", before : function(v) {
                return sprintf("%.1f", v);
            }},
            { name : "health_disbursements", type : "number", before : function(v) {
                return sprintf("%.1f", v);
            }},
            { name : "population", type : "number", before : function(v) {
                return sprintf("%.1f", v / 1000000);
            }},
            { name : "commitments_per_capita", type : "number", before : function(v) {
                return sprintf("%.1f", v);
            }},
            { name : "disbursements_per_capita", type : "number", before : function(v) {
                return sprintf("%.1f", v);
            }},
            { name : "total_commitments", type : "number", before : function(v) {
                return sprintf("%.1f", v);
            }},
            { name : "total_disbursements", type : "number", before : function(v) {
                return sprintf("%.1f", v);
            }},
            { name : "year", type : "number" }
        ]
    });

    var scorecard = this;
    ds.fetch({
        success: function() {
            console.log('Indicator dataset loaded');

            _.each(scorecard.all_years, function(year) {
                console.log("Indicator year: " + year);
                var base_year = scorecard.all_years[0]
                var dataidx = year - base_year
                var svgidx = year - base_year + 2; 

                var row = ds.rowByPosition(dataidx);
                var svg_map = {
                    "population" : 1,
                    "total_commitments" : 2,
                    "total_disbursements" : 3,
                    "health_commitments" : 4,
                    "health_disbursements" : 5,
                    "commitments_per_capita" : 8,
                    "disbursements_per_capita" : 9,
                    "external_resources" : 12,
                    "gghe_perc" : 13,
                    "gghe_cap" : 14
                }

                _.each(_.keys(svg_map), function(key) {
                    var id = svg_map[key]; 
                    var svg_id = "#col" + svgidx + "r" + id + " text";
                    d3.select(svg_id).text(row[key]);
                });
                
            });
            
        }
    });
};

ScorecardFrontPage.prototype.setup_allocation_block = function() {
    var ds = new Miso.Dataset({
        url : "/oda/data/allocation/" + this.iso3 + "/",
        parser : WHO.AllocationsParser,
        columns : [
            { name : "c_hpam", type : "number", before : function(v) {
                return sprintf("%.1f", v);
            }},
            { name : "c_mdg6", type : "number", before : function(v) {
                return sprintf("%.1f", v);
            }},
            { name : "c_ohp", type : "number", before : function(v) {
                return sprintf("%.1f", v);
            }},
            { name : "c_rhfp", type : "number", before : function(v) {
                return sprintf("%.1f", v);
            }},
            { name : "d_hpam", type : "number", before : function(v) {
                return sprintf("%.1f", v);
            }},
            { name : "d_mdg6", type : "number", before : function(v) {
                return sprintf("%.1f", v);
            }},
            { name : "d_ohp", type : "number", before : function(v) {
                return sprintf("%.1f", v);
            }},
            { name : "d_rhfp", type : "number", before : function(v) {
                return sprintf("%.1f", v);
            }},
            { name : "year", type : "number" }
        ]
    });

    var scorecard = this;
    ds.fetch({
        success: function() {
            console.log('Allocation dataset loaded');

            _.each(scorecard.all_years, function(year) {
                console.log("Allocation year: " + year);
                var base_year = scorecard.all_years[0]
                var dataidx = year - base_year
                var svgidx = year - base_year + 2; 

                var row = ds.rowByPosition(dataidx);
                var svg_map = {
                    "c_hpam" : 1, "c_mdg6" : 2, "c_ohp" : 3, "c_rhfp" : 4,
                    "d_hpam" : 1, "d_mdg6" : 2, "d_ohp" : 3, "d_rhfp" : 4
                }

                _.each(_.keys(svg_map), function(key) {
                    var id = svg_map[key]; 
                    if (key.startsWith("c_"))
                        var svg_id = "#Commitments #col" + svgidx + "r" + id + "_1_ text";
                    else
                        var svg_id = "#Disbursements #col" + svgidx + "r" + id + "_2_ text";
                    d3.select(svg_id).text(row[key]);
                });
            });
            
        }
    });
};

ScorecardFrontPage.prototype.generate_scorecord = function() {
    this.setup_country_name();
    this.setup_indicator_block();
    this.setup_allocation_block();
};


function scorecard_back(docroot) {
    alert('back');
}
