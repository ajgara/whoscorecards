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

var WHO = {};

// A parser that reformats the WHO indicator data from rows to columns
WHO.IndicatorsParser = function(data, options) {};
_.extend(
    WHO.IndicatorsParser.prototype, Miso.Parsers.Strict.prototype, Miso.Parsers.prototype,
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
            var country_name = d3.select("#_countryname_1_");
            country_name.text(this.column("Name").data[0]);
        }
    });
};

ScorecardFrontPage.prototype.setup_indicator_block = function() {
    var ds = new Miso.Dataset({
        url : "/oda/data/" + this.iso3 + "/",
        parser : WHO.IndicatorsParser,
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
            { name : "population", type : "in_millions", before : function(v) {
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

    ds.fetch({
        success: function() {
            console.log('Indicator dataset loaded');

            _.each([2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010], function(year) {
                console.log("Indicator year: " + year);
                var dataidx = year - 2000;
                var svgidx = year - 2000 + 2; 

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

ScorecardFrontPage.prototype.generate_scorecord = function() {
    this.setup_country_name();
    this.setup_indicator_block();
};


function scorecard_back(docroot) {
    alert('back');
}
