// Add a startWith method to strings
if (typeof String.prototype.startsWith != 'function') {
  String.prototype.startsWith = function (str){
    return this.indexOf(str) == 0;
  };
}

if (typeof Number.prototype.formatThousands != 'function') {
    Number.prototype.formatThousands = function(c, d, t) {
        var n = this, 
            c = isNaN(c = Math.abs(c)) ? 2 : c, 
            d = d == undefined ? "." : d, 
            t = t == undefined ? "," : t, 
            s = n < 0 ? "-" : "", 
            i = parseInt(n = Math.abs(+n || 0).toFixed(c)) + "", 
            j = (j = i.length) > 3 ? j % 3 : 0;
       return s 
              + (j ? i.substr(0, j) + t : "") 
              + i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + t) 
              + (c ? d + Math.abs(n - i).toFixed(c).slice(2) : "");
    }
}

round = function(x, places) {
    x = x * Math.pow(10, places);
    x = Math.round(x)
    x =  x / Math.pow(10, places);
    return x;
}


check_before_fmt = function(v, func) {
    if (v == undefined || isNaN(v))
        return "-";
    return func(v);
}

r0 = function(v) {
    return check_before_fmt(v, function(v) {return v.formatThousands(0);});
}

r0nt = function(v) {
    return check_before_fmt(v, Math.round(v));
}

r1 = function(v) {
    return check_before_fmt(v, function(v) {return v.formatThousands(1);});
}
r2 = function(v) {
    return check_before_fmt(v, function(v) {return v.formatThousands(2);});
}

r12 = function(v) {
    return check_before_fmt(v, function(v) {
        if (v < 1000000) 
            return v.formatThousands(2);
        return v.formatThousands(1);
    });
}

niz = function(v) {
    if (isNaN(v)) return 0;
    return v;
}

noz = function(v) {
    if (v == undefined)
        return 0
    return v
}


function load_front(json) {
    var country_name = d3.select("#countryname").text(json.country.name.toUpperCase());
    d3.select("#sum_increase").text(Math.round(json.summary.sum_increase) + "%");
    d3.select("#sum_label").text(json.summary.sum_label);
    d3.select("#sum_amount").text(r0(json.summary.sum_last_year) + "%");

    purpose_mapping = {
        "HEALTH POLICY & ADMIN. MANAGEMENT" : "Health Policy & Admin",
        "MDG6" : "MDG6",
        "Other Health Purposes" : "Other Health Purposes",
        "RH & FP" : "Reproductive H. & Family Planning"
    }
    d3.select("#sum_purpose").text(purpose_mapping[json.summary.sum_purpose]);
    d3.select("#sum_2000").text(Math.round(json.summary.sum_base_year) + "%");
    d3.select("#sum_baseyear").text(json.summary.sum_baseyear);

    var all_years = ["2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012"];
    _.each(all_years, function(el, i) {

        // *********************************************
        // General Information Section
        // *********************************************

        var indicators = json.indicators[el];
        d3.select("#indc" + (i + 2) + "r1").text(r12(indicators["Population as at 30 June"] / 1000000));
        d3.select("#indc" + (i + 2) + "r2").text(r2(indicators["Commitments TOTAL ODA (Million Constant 2012 US$)"]));
        d3.select("#indc" + (i + 2) + "r3").text(r2(indicators["Disbursements TOTAL ODA (Million Constant 2012 US$)"]));
        d3.select("#indc" + (i + 2) + "r4").text(r2(indicators["ODA for Health Commitments, (Million, Constant 2012 US$)"]));
        d3.select("#indc" + (i + 2) + "r5").text(r2(indicators["ODA for Health Disbursements, (Million, Constant 2012 US$)"]));
        d3.select("#indc" + (i + 2) + "r6").text(r2(indicators["RATIO Health/Total ODA Commitments"]));
        d3.select("#indc" + (i + 2) + "r7").text(r2(indicators["RATIO Health/Total ODA Disbursements"]));
        d3.select("#indc" + (i + 2) + "r8").text(r2(indicators["Health Commitments per Capita"]));
        d3.select("#indc" + (i + 2) + "r9").text(r2(indicators["Health Disbursements per Capita"]));
        d3.select("#indc" + (i + 2) + "r10").text(r2(indicators["Regional avg Health Commitments per Capita (const.2012 US$)"]));
        d3.select("#indc" + (i + 2) + "r11").text(r2(indicators["Regional avg Health Disbursements per Capita (const.2012 US$)"]));
        d3.select("#indc" + (i + 2) + "r12").text(r2(indicators["Total expenditure on health in current US$ per capita"]));
        d3.select("#indc" + (i + 2) + "r13").text(r2(indicators["General government expenditure on health in current US$ per capita"]));
        d3.select("#indc" + (i + 2) + "r14").text(r2(indicators["Private expenditure on health in current US$ per capita"]));


        var allocation_commitments = json.allocations.commitments[el];
        var allocation_disbursements = json.allocations.disbursements[el];

        d3.select("#allcc" + (i + 1) + "r1").text("-")
        d3.select("#allcc" + (i + 1) + "r2").text("-")
        d3.select("#allcc" + (i + 1) + "r3").text("-")
        d3.select("#allcc" + (i + 1) + "r4").text("-")
        d3.select("#allcc" + (i + 1) + "r5").text("-")

        if (allocation_commitments != undefined) {
            d3.select("#allcc" + (i + 1) + "r1").text(r2(allocation_commitments["HEALTH POLICY & ADMIN. MANAGEMENT"]));
            d3.select("#allcc" + (i + 1) + "r2").text(r2(allocation_commitments["MDG6"]));
            d3.select("#allcc" + (i + 1) + "r3").text(r2(allocation_commitments["Other Health Purposes"]));
            d3.select("#allcc" + (i + 1) + "r4").text(r2(allocation_commitments["RH & FP"]));
            d3.select("#allcc" + (i + 1) + "r5").text(r2(_.sum(_.values(allocation_commitments))));
        }

        d3.select("#alldc" + (i + 1) + "r1").text("-")
        d3.select("#alldc" + (i + 1) + "r2").text("-")
        d3.select("#alldc" + (i + 1) + "r3").text("-")
        d3.select("#alldc" + (i + 1) + "r4").text("-")
        d3.select("#alldc" + (i + 1) + "r5").text("-")

        if (allocation_disbursements != undefined) {
            d3.select("#alldc" + (i + 1) + "r1").text(r2(allocation_disbursements["HEALTH POLICY & ADMIN. MANAGEMENT"]));
            d3.select("#alldc" + (i + 1) + "r2").text(r2(allocation_disbursements["MDG6"]));
            d3.select("#alldc" + (i + 1) + "r3").text(r2(allocation_disbursements["Other Health Purposes"]));
            d3.select("#alldc" + (i + 1) + "r4").text(r2(allocation_disbursements["RH & FP"]));
            d3.select("#alldc" + (i + 1) + "r5").text(r2(_.sum(_.values(allocation_disbursements))));
        }

        // segment pie
        var segpie = {
            width: 31,
            height:31,

            arc: {
                margin: 25,
                width: 15,
            },
            colors : ["#cf3e96", "#62A73B", "#79317F", "#009983"],
            class : "piechart"
        };

        if (allocation_commitments != undefined) {
            segpie["node"] = "#piec_" + (2001 + i);
            segpie["data"] = [
                {"value" : niz(allocation_commitments["HEALTH POLICY & ADMIN. MANAGEMENT"])},
                {"value" : niz(allocation_commitments["MDG6"])},
                {"value" : niz(allocation_commitments["Other Health Purposes"])},
                {"value" : niz(allocation_commitments["RH & FP"])}
            ];
            
            var segpiegraph = new SegmentPieGraph(segpie);
        }
        d3.select("#piec_" + (2001 + i) + "_old").remove();

        if (allocation_disbursements != undefined) {
            segpie["node"] = "#pied_" + (2001 + i);
            segpie["data"] = [
                {"value" : niz(allocation_disbursements["HEALTH POLICY & ADMIN. MANAGEMENT"])},
                {"value" : niz(allocation_disbursements["MDG6"])},
                {"value" : niz(allocation_disbursements["Other Health Purposes"])},
                {"value" : niz(allocation_disbursements["RH & FP"])}
            ];
            var segpiegraph = new SegmentPieGraph(segpie);
        }
        
        d3.select("#pied_" + (2001 + i) + "_old").remove();

        
    });

    // bar charts
    var rounded = {
        bar: {
            'margin' : 4, // pixels between bars
            'width': 155, // width of bars
            'rounding': 5, // pixels for rounding effect
            'color': '#0093d5'
        },

        line: {
            const_val: '0'
        },
        width : 190,
        height : 102,
    }

    function arrow_change(indicator) {
        var val_penultimate_year = json.indicators["2011"][indicator];
        var val_last_year = json.indicators["2012"][indicator];
        var change = val_last_year - val_penultimate_year;
        return {
            increase : change,
            change : Math.abs(change)
        } 
    }

    function manipulate_arrow(arrow, change) {
        box = arrow + "_box2";
        if (change < 0) {
            d3.select(arrow).attr("style", "fill: #bf202e");
        } else if (change > 0) {
            d3.select(arrow).attr("style", "fill: #68ae45");
            d3.select(box).attr("transform", "matrix(1,0,0,-1,0,20)");
        }
    }

    function fmt_dollars(val) {
        return "$" + r2(val);
    }
    function fmt_millions(val) {
        return fmt_dollars(val) + "m";
    }

    /* --------- ODA for health commitments, per capita */

    
    max = _.reduce(all_years, function(memo, year) {
        var val = json.indicators[year]["ODA for Health Commitments, (Million, Constant 2012 US$)"];
        if (val > memo) memo = val;

        val = json.indicators[year]["ODA for Health Disbursements, (Million, Constant 2012 US$)"];
        if (val > memo) memo = val;

        return memo
        
    }, 0);
    rounded["node"] = "#oda_bar1"
    rounded["data"] = _.reduce(all_years, function(memo, year) {
        indicator = json.indicators[year]["ODA for Health Commitments, (Million, Constant 2012 US$)"];
            memo.push({"value" : round(noz(indicator), 2), "series" : year});
        return memo;
    }, [])
    rounded["max"] = max;
    var change = arrow_change("ODA for Health Commitments, (Million, Constant 2012 US$)");
    d3.select("#bar1_value").text(fmt_millions(change["change"]));
    manipulate_arrow("#bar1_arrow", change["increase"]);

    rbg = new RoundedBarGraph(rounded);
    d3.select("#oda_bar1_old").remove();

    /* --------- ODA for health disbursements, per capita */
    rounded["bar"]["color"] = "#df7627";
    rounded["node"] = "#oda_bar2"
    rounded["data"] = _.reduce(all_years, function(memo, year) {
        indicator = json.indicators[year]["ODA for Health Disbursements, (Million, Constant 2012 US$)"];
        memo.push({"value" : round(noz(indicator), 2), "series" : year});
        return memo;
    }, [])
    rounded["max"] = max;
    var change = arrow_change("ODA for Health Disbursements, (Million, Constant 2012 US$)");
    d3.select("#bar2_value").text(fmt_millions(change["change"]));
    manipulate_arrow("#bar2_arrow", change["increase"]);

    rbg = new RoundedBarGraph(rounded);
    d3.select("#oda_bar2_old").remove();

    /* --------- ODA for health commitments, per capita */
    max = _.reduce(all_years, function(memo, year) {
        var val = json.indicators[year]["Health Commitments per Capita"];
        if (val > memo) memo = val;

        val = json.indicators[year]["Health Disbursements per Capita"];
        if (val > memo) memo = val;

        val = json.indicators[year]["Regional avg Health Commitments per Capita (const.2012 US$)"];
        if (val > memo) memo = val;

        val = json.indicators[year]["Regional avg Health Disbursements per Capita (const.2012 US$)"];
        if (val > memo) memo = val;

        return memo
    }, 0);

    rounded["max"] = max;
    rounded["bar"]["color"] = "#0093d5";
    rounded["node"] = "#oda_bar3"
    rounded["data"] = _.reduce(all_years, function(memo, year) {
        indicator = json.indicators[year]["Health Commitments per Capita"];
        memo.push({"value" : round(noz(indicator), 2), "series" : year});
        return memo;
    }, [])
    rounded["line"] = {
        type : "point",
        data : _.reduce(all_years, function(memo, year) {
            var v = json.indicators[year]["Regional avg Health Commitments per Capita (const.2012 US$)"];
            memo.push(noz(v));
            return memo;
        }, [])
    }
    
    var change = arrow_change("Health Commitments per Capita");
    d3.select("#bar3_value").text(fmt_dollars(change["change"]));
    manipulate_arrow("#bar3_arrow", change["increase"]);

    rbg = new RoundedBarGraph(rounded);
    d3.select("#oda_bar3_old").remove();

    /* --------- ODA for health disbursements, per capita */
    rounded["bar"]["color"] = "#df7627";
    rounded["node"] = "#oda_bar4"
    rounded["data"] = _.reduce(all_years, function(memo, year) {
        indicator = json.indicators[year]["Health Disbursements per Capita"];
        memo.push({"value" : round(noz(indicator), 2), "series" : year});
        return memo;
    }, [])
    rounded["line"] = {
        type : "point",
        data : _.reduce(all_years, function(memo, year) {
            var v = json.indicators[year]["Regional avg Health Disbursements per Capita (const.2012 US$)"];
            memo.push(noz(v));
            return memo;
        }, [])
    }
    var change = arrow_change("Health Disbursements per Capita");
    d3.select("#bar4_value").text(fmt_dollars(change["change"]));
    manipulate_arrow("#bar4_arrow", change["increase"]);

    rbg = new RoundedBarGraph(rounded);
    d3.select("#oda_bar4_old").remove();

}
function load_back(json) {
    /*********** Country Name ************/
    var country_name = d3.select("#countryname").text(json.country.name.toUpperCase());
    d3.select("#summary_amount").text(r2(json.summary.total_disbursements_sum));
    d3.select("#summary_count").text(r0(json.summary.total_disbursements_count));

    var countries = [
        "Australia", "Austria", "Belgium", "Canada", "Czech Republic", "Denmark", 
        "Finland", "France", "Germany", "Greece", "Iceland", "Ireland",
        "Italy", "Japan", "Kuwait", "Luxembourg", "Netherlands", "New Zealand",
        "Norway", "Portugal", "Republic of Korea", "Spain", "Sweden", "Switzerland",
        "United Arab Emirates", "United Kingdom", "United States of America"
    ];

    var multis = [
        "AfDB", "AfDF", "Arab Fund (AFESD)", "AsDB Special Funds", "BADEA", "EU Institutions", "GAVI",
        "IDA", "IDB Sp. Fund", "OFID", "The Global Fund", "UNAIDS", "UNDP", "UNFPA", "UNICEF", "UNPBF", "UNRWA", "WFP", "WHO"
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
    
    var other_perc = json.largest_sources[json.largest_sources.length - 1]["percentage"]
    d3.select("#bubble_perc6").text(r1(other_perc * 100) + "%");
    

    var largest_value = json.largest_sources[0]["percentage"];
    // if the largest value not much larger than the other values, scale it down to prevent overlaps
    ratio1 = largest_value < 0.28 ? 0.78 : 1.0;
    ratio2 = Math.sqrt(json.largest_sources[1]["percentage"] / json.largest_sources[0]["percentage"]) * ratio1;
    ratio3 = Math.sqrt(json.largest_sources[2]["percentage"] / json.largest_sources[0]["percentage"]) * ratio1;
    ratio4 = Math.sqrt(json.largest_sources[3]["percentage"] / json.largest_sources[0]["percentage"]) * ratio1;
    ratio5 = Math.sqrt(json.largest_sources[4]["percentage"] / json.largest_sources[0]["percentage"]) * ratio1;
    ratio6 = Math.sqrt(other_perc / json.largest_sources[0]["percentage"]) * ratio1;

    other_disbursements = 100 - totaltop5;

    d3.select("#bubble1").attr("transform", "scale(" + ratio1 + "," + ratio1 + ")");
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

    var val1 = r0(json.disbursements_percentage["other"].percentage * 100);
    var val2 = r0(json.disbursements_percentage["largest"].percentage * 100);
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
