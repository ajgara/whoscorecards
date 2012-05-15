// Add a startWith method to strings
if (typeof String.prototype.startsWith != 'function') {
  String.prototype.startsWith = function (str){
    return this.indexOf(str) == 0;
  };
}
var WHO = {};

// A parser that reformats the WHO indicator data from rows to columns
// Better would be a generic parser that re-shapes the data by denormalising it according to a specific column
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
                "total_expenditure", 
                "gge", "private_expenditure"
            ],
            dataColumns = {
                population : [], 
                total_commitments : [], 
                total_disbursements : [], 
                health_commitments : [], 
                health_disbursements : [], 
                ratio_commitments : [], 
                ratio_disbursements : [], 
                commitments_per_capita : [], 
                disbursements_per_capita : [], 
                regional_avg_commitements : [], 
                regional_avg_disbursements : [], 
                total_expenditure : [], 
                gge : [], 
                private_expenditure : [],
                year : []
            }

            // TODO see if this can be simplified
            data.sort(function(a, b) {
                if (a.year < b.year) return -1;
                if (a.year > b.year) return 1;
                return 0;
            });

            var indicator_map = {
                1 : "regional_disb",
                2 : "regional_comm",
                3 : "regional_disb_ratio",
                4 : "regional_comm_ratio",
                5 : "population",
                6 : "health_disbursements",
                7 : "health_commitments",
                8 : "total_disbursements",
                9 : "disbursements_per_capita",
                10 : "total_commitments",
                11 : "commitments_per_capita",
                12 : "total_expenditure",
                13 : "gge",
                14 : "private_expenditure",
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

WHO.ScorecardData = function(iso3, base_url) {
    this.iso3 = iso3;
    this.base_url = base_url;
    this._fetchAll();
};

WHO.ScorecardData.prototype = {
    _round1 : function(v) { return sprintf("%.1f", v); },
    _round1perc : function(v) { return sprintf("%.1f%%", v * 100); },
    _round1mill : function(v) { return sprintf("%.1f", v / 1000000); },
    _getCountryName : function() {
        return new Miso.Dataset({
            url : this.base_url + "/oda/data/country_name/" + this.iso3 + "/"
        }).fetch();
    },
    _getIndicatorData : function() {
        return new Miso.Dataset({
            url : this.base_url + "/oda/data/" + this.iso3 + "/",
            parser : WHO.IndicatorsParser,
            columns : [
                { name : "gge", type : "string", before : this._round1perc },
                { name : "private_expenditure", type : "number", before : this._round1 },
                { name : "total_expenditure", type : "string", before : this._round1perc },
                { name : "health_commitments", type : "number", before : this._round1 },
                { name : "health_disbursements", type : "number", before : this._round1 },
                { name : "population", type : "number", before : this._round1mill },
                { name : "commitments_per_capita", type : "number", before : this._round1 },
                { name : "disbursements_per_capita", type : "number", before : this._round1 },
                { name : "total_commitments", type : "number", before : this._round1},
                { name : "total_disbursements", type : "number", before : this._round1 },
                { name : "year", type : "number" }
            ]
        }).fetch();
    },
    _getAllocationData : function() {
        return new Miso.Dataset({
            url : this.base_url + "/oda/data/allocation/" + this.iso3 + "/",
            parser : WHO.AllocationsParser,
            columns : [
                { name : "c_hpam", type : "number", before : this._round1 },
                { name : "c_mdg6", type : "number", before : this._round1 },
                { name : "c_ohp", type : "number", before : this._round1 },
                { name : "c_rhfp", type : "number", before : this._round1 },
                { name : "d_hpam", type : "number", before : this._round1 },
                { name : "d_mdg6", type : "number", before : this._round1 },
                { name : "d_ohp", type : "number", before : this._round1 },
                { name : "d_rhfp", type : "number", before : this._round1 },
                { name : "year", type : "number" }
            ]
        }).fetch();
    },
    _fetchAll : function() {
        this.countryName = this._getCountryName();
        this.indicatorData = this._getIndicatorData();
        this.allocationData = this._getAllocationData();
    }  
};

WHO.ScorecardFrontPage = function(docroot, iso3, base_url) {
    this.docroot = docroot;
    this.iso3 = iso3;
    this.all_years = [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010];
    this.data = new WHO.ScorecardData(iso3, base_url);
}

WHO.ScorecardFrontPage.prototype = {
    setup_country_name : function() {
        this.data.countryName.done(function(ds) {
            console.log('Country name dataset loaded');
            var country_name = d3.select("#_countryname_1_");
            country_name.text(ds.column("Name").data[0].toUpperCase());
        });
    },
    setup_indicator_block : function() {
        var scorecard = this;
        this.data.indicatorData.done(function(ds) {
            // Loop over each year
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
                    "total_expenditure" : 12,
                    "gge" : 13,
                    "private_expenditure" : 14
                }

                // Update each indicator in the current year
                _.each(_.keys(svg_map), function(key) {
                    var id = svg_map[key]; 
                    var svg_id = "#col" + svgidx + "r" + id + " text";
                    d3.select(svg_id).text(row[key]);
                });
            });
        });
    },
    setup_allocation_block : function() {
        var scorecard = this;
        this.data.allocationData.done(function(ds) {
            // Loop over each year
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
        });
    },
    setup_graph_block : function() {
        var scorecard = this;
        var rounded = {
            bar: {
                'margin' : 4, // pixels between bars
                'width': 185, // width of bars
                'rounding': 3, // pixels for rounding effect
                'color': '#0093d5'
            },

            line: {
                const_val: '0'
            }
        }
        function gen_graph(parent_node, series_name, ctx) {
            scorecard.data.indicatorData.done(function(ds) {
                var graph_selector = parent_node + " .graph_container";
                var graph_container = d3.select(graph_selector);
                var bbox = graph_container.node().getBBox();

                ctx["node"] = graph_selector;

                ctx["width"] = bbox.width;
                ctx["height"] = bbox.height;
                ctx["width"] = 169.513;
                ctx["height"] = 92.924;

                var data_series = ds.column(series_name).data;
                var pairs = _.zip(data_series, scorecard.all_years);
                ctx["data"] = _.reduce(pairs, function(memo, pair) {
                    memo.push({"value" : pair[0], "series" : pair[1]});
                    return memo;
                }, []);


                graph_container.remove();
                d3.select(parent_node).append("g")
                    .attr("transform", "translate(" + bbox.x + "," + bbox.y + ")")
                    .attr("class", "graph_container")

            
                rbg = new RoundedBarGraph(ctx)

                d3.selectAll(parent_node + " .rb-series").attr("dy", -2);
            });
        }
        gen_graph("#bargraph1_block", "total_commitments", rounded);
        gen_graph("#bargraph2_block", "total_disbursements", rounded);
        gen_graph("#bargraph3_block", "commitments_per_capita", rounded);
        gen_graph("#bargraph4_block", "disbursements_per_capita", rounded);
    },
    setup_piecharts : function() {
        var scorecard = this;
        var context = {}

        function gen_graph(node, series_name, ctx) {
            scorecard.data.allocationData.done(function(ds) {
                d3_node = d3.select(node);
                console.log(node);
                console.log(d3_node);
                console.log(d3.select(d3_node));
                var bbox = d3_node.node().getBBox();
                var d3_parent_node = d3_node[0][0].parentNode;

                ctx["node"] = d3_parent_node;

                ctx["width"] = bbox.width * 2;
                ctx["height"] = bbox.height * 2;
                ctx["radius"] = 20;
                ctx["data"] = [
                    {"label" : "", "value" : 20},
                    {"label" : "", "value" : 50},
                    {"label" : "", "value" : 30},
                    {"label" : "", "value" : 40}
                ]

                pie = new Piechart(ctx);

                d3_node.select(".piechart").attr("transform", "translate(" + 500 + "," + 0 + ")")
                d3_node.remove()
                return;
                /*


                var data_series = ds.column(series_name).data;
                var pairs = _.zip(data_series, scorecard.all_years);
                ctx["data"] = _.reduce(pairs, function(memo, pair) {
                    memo.push({"value" : pair[0], "series" : pair[1]});
                    return memo;
                }, []);


                graph_container.remove();
                d3.select(parent_node).append("g")
                    .attr("transform", "translate(" + bbox.x + "," + bbox.y + ")")
                    .attr("class", "graph_container")

            
                rbg = new RoundedBarGraph(ctx)

                d3.selectAll(parent_node + " .rb-series").attr("dy", -2);
                */
            });
        }
        gen_graph("#pie2000c", "", context);
        gen_graph("#pie2001c", "", context);
        gen_graph("#pie2002c", "", context);
        gen_graph("#pie2003c", "", context);
        gen_graph("#pie2004c", "", context);
        gen_graph("#pie2005c", "", context);
        gen_graph("#pie2006c", "", context);
        gen_graph("#pie2007c", "", context);
        gen_graph("#pie2008c", "", context);
        gen_graph("#pie2009c", "", context);
        gen_graph("#pie2010c", "", context);

        gen_graph("#pie2000d", "", context);
        gen_graph("#pie2001d", "", context);
        gen_graph("#pie2002d", "", context);
        gen_graph("#pie2003d", "", context);
        gen_graph("#pie2004d", "", context);
        gen_graph("#pie2005d", "", context);
        gen_graph("#pie2006d", "", context);
        gen_graph("#pie2007d", "", context);
        gen_graph("#pie2008d", "", context);
        gen_graph("#pie2009d", "", context);
        gen_graph("#pie2010d", "", context);
    },
    generate_scorecord : function() {
        this.setup_country_name();
        this.setup_indicator_block();
        this.setup_allocation_block();
        this.setup_graph_block();
        //this.setup_piecharts();
    }
}


function scorecard_back(docroot) {
    alert('back');
}

round1 = function(v) { return sprintf("%.1f", v); }
round1perc = function(v) { return sprintf("%.1f%%", v * 100); }
round1mill = function(v) { return sprintf("%.1f", v / 1000000); }

function load_json(json) {
    /*********** Country Name ************/
    var country_name = d3.select("#_countryname_1_").text(json.country.name.toUpperCase());
    var all_years = ["2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010"];

    /*********** Indicators Table ************/
    var imap = {
        "1" : { value : "5", fmt : round1mill},
        "2" : { value : "10", fmt : round1},
        "3" : { value : "8", fmt : round1},
        "4" : { value : "7", fmt : round1},
        "5" : { value : "6", fmt : round1},
        "6" : { value : "4", fmt : round1},
        "7" : { value : "3", fmt : round1},
        "8" : { value : "11", fmt : round1},
        "9" : { value : "9", fmt : round1},
        "10" : { value : "2", fmt : round1},
        "11" : { value : "1", fmt : round1},
        "12" : { value : "12", fmt : round1},
        "13" : { value : "13", fmt : round1},
        "14" : { value : "14", fmt : round1},
    }

    _.each(all_years, function(year) {
        var col_class = ".ind_" + year + " text";
        d3.selectAll(col_class).data(_.keys(json.indicators[year]))
            .text(function(d, i) {
                var idx = imap[String(i + 1)];
                return idx.fmt(json.indicators[year][idx.value]);
            });
    });

    /*********** Allocation Table ************/
    var amap = {
        "0" : { value : "0", fmt : round1},
        "1" : { value : "1", fmt : round1},
        "2" : { value : "2", fmt : round1},
        "3" : { value : "3", fmt : round1},
    }

    _.each(all_years, function(year) {
        var col_class = ".allocation_c_" + year + " text";
        /* commitments */
        commitments = d3.selectAll(col_class).data(_.keys(json.allocations[year]));
        commitments
            .text(function(d, i) {
                var idx = amap[String(i)];
                return idx.fmt(json.allocations[year][idx.value].commitment);
            });

        commitments.exit().text(function(d, i) {
            val = _.reduce(json.allocations[year], function(memo, el) {
                return memo + el.commitment
            }, 0);
            return round1(val);
        });

        

        var pies = d3.selectAll(".piec g").data(all_years);
        pies.selectAll("g").remove();
        _.each(pies, function(el) {
            if (!el) return;
            console.log(el.id);
            ctx = {
                width : 200,
                height : 200,
                radius : 50,
                node : el.id,
                data : [
                    {"label":"one", "value":20}, 
                    {"label":"two", "value":50}, 
                    {"label":"three", "value":30}
                ]
            }
            Piechart(ctx);
        });

        /* disbursements */
        col_class = ".allocation_d_" + year + " text";
        disbursements = d3.selectAll(col_class).data(_.keys(json.allocations[year]));
        disbursements
            .text(function(d, i) {
                var idx = amap[String(i)];
                return idx.fmt(json.allocations[year][idx.value].disbursement);
            });

        disbursements.exit().text(function(d, i) {
            val = _.reduce(json.allocations[year], function(memo, el) {
                return memo + el.disbursement
            }, 0);
            return round1(val);
        });
    });
}

r0 = function(v) { return sprintf("%.0f", v); }
r1 = function(v) { return sprintf("%.1f", v); }
r2 = function(v) { return sprintf("%.2f", v); }

function load_back(json) {
    /*********** Country Name ************/
    var country_name = d3.select("#countryname").text(json.country.name.toUpperCase());
    d3.select("#summary_amount").text(r2(json.summary.total_disbursements_sum));
    d3.select("#summary_count").text(r0(json.summary.total_disbursements_count));

    var countries = [
        "Australia", "Austria", "Belgium", "Canada", "Denmark", 
        "Finland", "France", "Germany", "Greece", "Ireland",
        "Italy", "Japan", "Korea", "Luxembourg", "Netherlands",
        "Norway", "Spain", "Sweden", "Switzerland", "United Arab Emirates",
        "United Kingdom", "United States"
    ];

    var multis = [
        "AfDF", "AFESD", "AsDB Special Fund", "EU Institutions", "GAVI",
        "GEF", "Global Fund", "IDA", "IDB Special Fund", "OFID", "UNAIDS",
        "UNDP", "UNFPA", "UNICEF", "UNPBF", "UNRWA", "UNRWA", "UNRWA", "UNRWA", "WFP"
    ]

    var bil_total_nr = 0;
    var bil_total_value = 0;
    // bilateral and multilateral tables
    _.each(countries, function(c, i) {
        d3.select("#col2r" + (i + 1)).text("-");
        d3.select("#col3r" + (i + 1)).text("-");
        if (json.bil_sources[c] != undefined) {
            d3.select("#col2r" + (i + 1)).text(json.bil_sources[c].number);
            d3.select("#col3r" + (i + 1)).text(r2(json.bil_sources[c].amount));
            bil_total_nr += json.bil_sources[c].number;
            bil_total_value += json.bil_sources[c].amount;
        }
    });
    d3.select("#bil_total_nr").text(bil_total_nr);
    d3.select("#bil_total_value").text(r2(bil_total_value));

    var mul_total_nr = 0;
    var mul_total_value = 0;
    _.each(multis, function(c, i) {
        d3.select("#mcol2r" + (i + 1)).text("-");
        d3.select("#mcol3r" + (i + 1)).text("-");
        if (json.mul_sources[c] != undefined) {
            d3.select("#mcol2r" + (i + 1)).text(json.mul_sources[c].number);
            d3.select("#mcol3r" + (i + 1)).text(r2(json.mul_sources[c].amount));
            mul_total_nr += json.mul_sources[c].number;
            mul_total_value += json.mul_sources[c].amount;
        }
    });
    d3.select("#mul_total_nr").text(mul_total_nr);
    d3.select("#mul_total_value").text(r2(mul_total_value));

    // bubbles
    d3.select("#bubble_text1").text(json.largest_sources[0]["source"]);
    d3.select("#bubble_text2").text(json.largest_sources[1]["source"]);
    d3.select("#bubble_text3").text(json.largest_sources[2]["source"]);
    d3.select("#bubble_text4").text(json.largest_sources[3]["source"]);
    d3.select("#bubble_text5").text(json.largest_sources[4]["source"]);
    d3.select("#bubble_perc1").text(r1(json.largest_sources[0]["percentage"] * 100) + "%");
    d3.select("#bubble_perc2").text(r1(json.largest_sources[1]["percentage"] * 100) + "%");
    d3.select("#bubble_perc3").text(r1(json.largest_sources[2]["percentage"] * 100) + "%");
    d3.select("#bubble_perc4").text(r1(json.largest_sources[3]["percentage"] * 100) + "%");
    d3.select("#bubble_perc5").text(r1(json.largest_sources[4]["percentage"] * 100) + "%");

    var totaltop5 = _.reduce([0, 1, 2, 3, 4], function(memo, pair) {
        return memo + json.largest_sources[pair]["percentage"]
    }, 0);
    var other_perc = 1 - totaltop5;
    d3.select("#bubble_perc6").text(r1(other_perc * 100) + "%");
    

    ratio2 = Math.sqrt(json.largest_sources[1]["percentage"] / json.largest_sources[0]["percentage"]);
    ratio3 = Math.sqrt(json.largest_sources[2]["percentage"] / json.largest_sources[0]["percentage"]);
    ratio4 = Math.sqrt(json.largest_sources[3]["percentage"] / json.largest_sources[0]["percentage"]);
    ratio5 = Math.sqrt(json.largest_sources[4]["percentage"] / json.largest_sources[0]["percentage"]);
    ratio6 = Math.sqrt(other_perc / json.largest_sources[0]["percentage"]);

    other_disbursements = 100 - totaltop5;

    d3.select("#bubble2").attr("transform", "scale(" + ratio2 + "," + ratio2 + ")");
    d3.select("#bubble3").attr("transform", "scale(" + ratio3 + "," + ratio3 + ")");
    d3.select("#bubble4").attr("transform", "scale(" + ratio4 + "," + ratio4 + ")");
    d3.select("#bubble5").attr("transform", "scale(" + ratio5 + "," + ratio5 + ")");
    d3.select("#bubble6").attr("transform", "scale(" + ratio6 + "," + ratio6 + ")");

    // largest single disbursements
    _.each(json.largest_disbursements, function(el, i) {
        d3.select("#sdcol1r" + (i + 1)).text("$" + r2(el.disbursement) + "m");
        d3.select("#sdcol2r" + (i + 1)).text(el.year);
        d3.select("#sdcol3r" + (i + 1)).text(el.donor.toUpperCase());
        d3.select("#sdcol4r" + (i + 1)).text(el.purpose);
    }); 

    var val1 = r1(json.disbursements_percentage["other"].percentage * 100);
    var val2 = r1(json.disbursements_percentage["largest"].percentage * 100);
    // segment pie
    var segpie = {
        width: 300,
        height:300,
        node :'#segpie',

        arc: {
            margin: 25,
            width: 74,
        },
        data : [
            {'value': parseInt(val1)},
            {'value': parseInt(val2)},
        ],
        colors : [
            "#0093D5", "#009983"
        ]
    };
    var _attr = d3.select("#segpie").attr("transform");
    d3.select("#segpie").attr("transform", "scale(0.35, 0.35)");
    
    var segpiegraph = new SegmentPieGraph(segpie);
    var chart = d3.select("#segpie svg g");
    d3.select("#oldpie").remove();

    d3.select("#largest_other_text").text(json.summary.total_disbursements_count - 7);
    

}
