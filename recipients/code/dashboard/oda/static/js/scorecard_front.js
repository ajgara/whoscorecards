function fillIndicatorsTable(indicators) {
    var data = indicators.data;
    var names = indicators.names;
    var years = indicators.years;

    for(var i = 0; i < years.length; i++) {
        for(var j = 0; j < names.length; j++) {
            d3.select("#indc" + (i + 2) + "r" + (j + 1)).text(data[years[i]][names[j]]["formatted"]);
        }
    }
}

function fillCommitmentPurposeTable(commitment_purpose_table) {
    var data = commitment_purpose_table.data;
    var names = commitment_purpose_table.names;
    var years = commitment_purpose_table.years;

    for(var i = 0; i < years.length; i++) {
        for(var j = 0; j < names.length; j++) {
            d3.select("#allcc" + (i + 1) + "r" + (j + 1)).text(data[years[i]][names[j]]["formatted"]);
        }
    }
}

function createCommitmentTablePies(commitment_purpose_table) {
    var data = commitment_purpose_table.data;
    var names = commitment_purpose_table.names;
    var years = commitment_purpose_table.years;

    var pieOptions = {
        width: 31,
        height:31,
        arc: {margin: 25, width: 15},
        colors: ["#cf3e96", "#62A73B", "#79317F", "#009983"],
        class: "piechart"
    };

    for(var i = 0; i < years.length; i++) {
        pieOptions["node"] = "#piec_" + (2001 + i);
        pieOptions["data"] = [];

        for(var j = 0; j < names.length - 1; j++) {
            pieOptions["data"].push({"value": data[years[i]][names[j]]["real"]});
        }

        var segpiegraph = new SegmentPieGraph(pieOptions);
        d3.select("#piec_" + (2001 + i) + "_old").remove();
    }
}

function fillDisbursementPurposeTable(disbursement_purpose_table) {
    var data = disbursement_purpose_table.data;
    var names = disbursement_purpose_table.names;
    var years = disbursement_purpose_table.years;

    for(var i = 0; i < years.length; i++) {
        for(var j = 0; j < names.length; j++) {
            d3.select("#alldc" + (i + 1) + "r" + (j + 1)).text(data[years[i]][names[j]]["formatted"]);
        }
    }
}

function createDisbursementTablePies(disbursement_purpose_table) {
    var data = disbursement_purpose_table.data;
    var names = disbursement_purpose_table.names;
    var years = disbursement_purpose_table.years;

    var pieOptions = {
        width: 31,
        height:31,
        arc: {margin: 25, width: 15},
        colors: ["#cf3e96", "#62A73B", "#79317F", "#009983"],
        class: "piechart"
    };

    for(var i = 0; i < years.length; i++) {
        pieOptions["node"] = "#pied_" + (2001 + i);
        pieOptions["data"] = [];

        for(var j = 0; j < names.length - 1; j++) {
            pieOptions["data"].push({"value": data[years[i]][names[j]]["real"]});
        }

        var segpiegraph = new SegmentPieGraph(pieOptions);
        d3.select("#pied_" + (2001 + i) + "_old").remove();
    }
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

    fillIndicatorsTable(json.indicator_table);
    fillCommitmentPurposeTable(json.commitment_purpose_table);
    fillDisbursementPurposeTable(json.disbursement_purpose_table);
    createCommitmentTablePies(json.commitment_purpose_table);
    createDisbursementTablePies(json.disbursement_purpose_table);

    var all_years = ["2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012"];

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