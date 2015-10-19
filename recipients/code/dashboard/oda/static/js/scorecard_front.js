function manipulate_arrow(arrow, change) {
    box = arrow + "_box2";
    if (change < 0) {
        d3.select(arrow).attr("style", "fill: #bf202e");
    } else if (change > 0) {
        d3.select(arrow).attr("style", "fill: #68ae45");
        d3.select(box).attr("transform", "matrix(1,0,0,-1,0,20)");
    }
}

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

function createFirstBarGraph(indicator_table) {
    var years = indicator_table.years;
    var data = indicator_table.data;

    var maxValue = 0;
    for(var i = 0; i < years.length; i++) {
        var aux = data[years[i]]["ODA Commitments Health"]["real"];
        if(maxValue < aux) maxValue = aux;
        aux = data[years[i]]["ODA Disbursements Health"]["real"];
        if(maxValue < aux) maxValue = aux;
    }

    var barOptions = {
        bar: {'margin': 4, 'width': 155, 'rounding': 5, 'color': '#0093d5'},
        line: {const_val: '0'}, width : 190, height : 102
    };

    barOptions["node"] = "#oda_bar1"
    var values = [];
    for(i = 0; i < years.length; i++) {
        var value = data[years[i]]["ODA Commitments Health"]["real"];
        values.push({"value": round(noz(value), 2), "series": years[i]});
    }
    barOptions["data"] = values;
    barOptions["max"] = maxValue;

    var lastYear = data[years[years.length - 1]]["ODA Commitments Health"]["real"];
    var lastLastYear = data[years[years.length - 2]]["ODA Commitments Health"]["real"];
    var increase = lastYear - lastLastYear;
    var change = Math.abs(increase);
    d3.select("#bar1_value").text(fmt_millions(change));
    manipulate_arrow("#bar1_arrow", increase);
    rbg = new RoundedBarGraph(barOptions);
    d3.select("#oda_bar1_old").remove();
}

function createSecondBarGraph(indicator_table) {
    var years = indicator_table.years;
    var data = indicator_table.data;

    var maxValue = 0;
    for(var i = 0; i < years.length; i++) {
        var aux = data[years[i]]["ODA Commitments Health"]["real"];
        if(maxValue < aux) maxValue = aux;
        aux = data[years[i]]["ODA Disbursements Health"]["real"];
        if(maxValue < aux) maxValue = aux;
    }

    var barOptions = {
        bar: {'margin': 4, 'width': 155, 'rounding': 5, 'color': '#df7627'},
        line: {const_val: '0'}, width : 190, height : 102
    };

    barOptions["node"] = "#oda_bar2";
    var values = [];
    for(i = 0; i < years.length; i++) {
        var value = data[years[i]]["ODA Disbursements Health"]["real"];
        values.push({"value": round(noz(value), 2), "series": years[i]});
    }
    barOptions["data"] = values;
    barOptions["max"] = maxValue;

    var lastYear = data[years[years.length - 1]]["ODA Disbursements Health"]["real"];
    var lastLastYear = data[years[years.length - 2]]["ODA Disbursements Health"]["real"];
    var increase = lastYear - lastLastYear;
    var change = Math.abs(increase);
    d3.select("#bar2_value").text(fmt_millions(change));
    manipulate_arrow("#bar2_arrow", increase);
    rbg = new RoundedBarGraph(barOptions);
    d3.select("#oda_bar2_old").remove();
}

function createThirdBarGraph(indicator_table) {
    var years = indicator_table.years;
    var data = indicator_table.data;

    var maxValue = 0;
    for(var i = 0; i < years.length; i++) {
        var aux = data[years[i]]["Regional Avg Health Commitments per Capita"]["real"];
        if(maxValue < aux) maxValue = aux;
        aux = data[years[i]]["Regional Avg Health Disbursements per Capita"]["real"];
        if(maxValue < aux) maxValue = aux;
        aux = data[years[i]]["Health Commitments per Capita"]["real"];
        if(maxValue < aux) maxValue = aux;
        aux = data[years[i]]["Health Disbursements per Capita"]["real"];
        if(maxValue < aux) maxValue = aux;
    }

    var barOptions = {
        bar: {'margin': 4, 'width': 155, 'rounding': 5, 'color': '#0093d5'},
        line: {const_val: '0'}, width : 190, height : 102
    };

    barOptions["node"] = "#oda_bar3";
    var values = [];
    for(i = 0; i < years.length; i++) {
        var value = data[years[i]]["Health Commitments per Capita"]["real"];
        values.push({"value": round(noz(value), 2), "series": years[i]});
    }
    barOptions["data"] = values;
    barOptions["max"] = maxValue;

    values = [];
    for(i = 0; i < years.length; i++) {
        var value = data[years[i]]["Regional Avg Health Commitments per Capita"]["real"];
        values.push(noz(value));
    }
    barOptions["line"] = {type: "point", data :values};

    var lastYear = data[years[years.length - 1]]["Health Commitments per Capita"]["real"];
    var lastLastYear = data[years[years.length - 2]]["Health Commitments per Capita"]["real"];
    var increase = lastYear - lastLastYear;
    var change = Math.abs(increase);
    d3.select("#bar3_value").text(fmt_dollars(change));
    manipulate_arrow("#bar3_arrow", increase);
    rbg = new RoundedBarGraph(barOptions);
    d3.select("#oda_bar3_old").remove();
}

function createFourthBarGraph(indicator_table) {
    var years = indicator_table.years;
    var data = indicator_table.data;

    var maxValue = 0;
    for(var i = 0; i < years.length; i++) {
        var aux = data[years[i]]["Regional Avg Health Commitments per Capita"]["real"];
        if(maxValue < aux) maxValue = aux;
        aux = data[years[i]]["Regional Avg Health Disbursements per Capita"]["real"];
        if(maxValue < aux) maxValue = aux;
        aux = data[years[i]]["Health Commitments per Capita"]["real"];
        if(maxValue < aux) maxValue = aux;
        aux = data[years[i]]["Health Disbursements per Capita"]["real"];
        if(maxValue < aux) maxValue = aux;
    }

    var barOptions = {
        bar: {'margin': 4, 'width': 155, 'rounding': 5, 'color': '#df7627'},
        line: {const_val: '0'}, width : 190, height : 102
    };

    barOptions["node"] = "#oda_bar4";
    var values = [];
    for(i = 0; i < years.length; i++) {
        var value = data[years[i]]["Health Disbursements per Capita"]["real"];
        values.push({"value": round(noz(value), 2), "series": years[i]});
    }
    barOptions["data"] = values;
    barOptions["max"] = maxValue;

    values = [];
    for(i = 0; i < years.length; i++) {
        var value = data[years[i]]["Regional Avg Health Disbursements per Capita"]["real"];
        values.push(noz(value));
    }
    barOptions["line"] = {type: "point", data :values};

    var lastYear = data[years[years.length - 1]]["Health Disbursements per Capita"]["real"];
    var lastLastYear = data[years[years.length - 2]]["Health Disbursements per Capita"]["real"];
    var increase = lastYear - lastLastYear;
    var change = Math.abs(increase);
    d3.select("#bar4_value").text(fmt_dollars(change));
    manipulate_arrow("#bar4_arrow", increase);
    rbg = new RoundedBarGraph(barOptions);
    d3.select("#oda_bar4_old").remove();
}

function load_front(json) {
    d3.select("#countryname").text(json.country.name.toUpperCase());
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
    // Added by BSG in order to display base year for Other Health Purposes text on top
    d3.select("#sum_baseyear_other").text(json.summary.sum_baseyear);

    fillIndicatorsTable(json.indicator_table);

    fillCommitmentPurposeTable(json.commitment_purpose_table);
    createCommitmentTablePies(json.commitment_purpose_table);

    fillDisbursementPurposeTable(json.disbursement_purpose_table);
    createDisbursementTablePies(json.disbursement_purpose_table);

    createFirstBarGraph(json.indicator_table);
    createSecondBarGraph(json.indicator_table);
    createThirdBarGraph(json.indicator_table);
    createFourthBarGraph(json.indicator_table);
}