
function fillTable(selector, table_data) {
    for(var i = 0; i < table_data.sources.length - 1; i++) {
        var source = table_data.sources[i];
        var number = table_data.data[source]['number_of_disbursements'];
        var amount = table_data.data[source]['amount']['formatted'];
        d3.select(selector + "1r" + (i + 1)).text(source);
        d3.select(selector + "2r" + (i + 1)).text(number);
        d3.select(selector + "3r" + (i + 1)).text(amount);
    }
}

function fillBilateralTotal(data) {
    var total_name = data.sources[data.sources.length - 1];
    var number = data.data[total_name]['number_of_disbursements'];
    var amount = data.data[total_name]['amount']['formatted'];
    d3.select("#bil_total_nr").text(number);
    d3.select("#bil_total_value").text(amount);
}

function fillMultilateralAndFoundationTotal(data) {
    var total_name = data.sources[data.sources.length - 1];
    var number = data.data[total_name]['number_of_disbursements'];
    var amount = data.data[total_name]['amount']['formatted'];
    d3.select("#mul_total_nr").text(number);
    d3.select("#mul_total_value").text(amount);
}

function createBubbleGraph(data) {
    for(var i = 0; i < 5; i++) {
        d3.select("#bubble_text" + (i + 1)).text(data[i]["name"]);
        d3.select("#bubble_perc" + (i + 1)).text(data[i]["percentage"]["formatted"]);
    }

    d3.select("#bubble_perc6").text(data[data.length - 1]["percentage"]["formatted"]);

    var largest_value = data[0]["percentage"]["real"];

    // if the largest value not much larger than the other values, scale it down to prevent overlaps
    var first_ratio = largest_value < 0.28 ? 0.78 : 1.0;
    var ratios = [first_ratio];

    for(i = 0; i < 5; i++) {
        var value = Math.sqrt(data[i + 1]["percentage"]["real"] / data[0]["percentage"]["real"]) * first_ratio;
        ratios.push(value);
    }

    for(i = 0; i < ratios.length; i++) {
        d3.select("#bubble" + (i + 1)).attr("transform", "scale(" + ratios[i] + "," + ratios[i] + ")");
    }
}

function fillSevenLargestDisbursementsTable(data) {
    for(var i = 0; i < data.length; i++) {
        d3.select("#sdcol1r" + (i + 1)).text(data[i]["disbursement"]);
        d3.select("#sdcol2r" + (i + 1)).text(data[i]["year"]);
        d3.select("#sdcol3r" + (i + 1)).text(data[i]["donor"]);
        d3.select("#sdcol4r" + (i + 1)).text(data[i]["purpose"]);
    }
}

function createSevenLargestDisbursementsGraph(data) {
    var other_percentage = data["other"]["percentage"]["formatted"];
    var largest_percentage = data["largest"]["percentage"]["formatted"];

    var pieOptions = {
        width: 300, height:300,
        node: '#segpie',
        arc: {margin: 25, width: 74},
        data: [{'value': parseInt(other_percentage)}, {'value': parseInt(largest_percentage)}],
        colors: ["#0093D5", "#009983"]
    };

    var _attr = d3.select("#segpie").attr("transform");
    d3.select("#segpie").attr("transform", "scale(0.35, 0.35)");

    var segpiegraph = new SegmentPieGraph(pieOptions);
    var chart = d3.select("#segpie svg g");
    d3.select("#oldpie").remove();
}

function load_back(json) {
    /*********** Country Name ************/
    var country_name = d3.select("#countryname").text(json.country.name.toUpperCase());
    d3.select("#summary_amount").text(r2(json.summary.total_disbursements_sum));
    d3.select("#summary_count").text(r0(json.summary.total_disbursements_count));

    fillTable("#col", json.bilateral_table);
    fillTable("#mcol", json.multilateral_and_foundation_table);

    fillBilateralTotal(json.bilateral_table);
    fillMultilateralAndFoundationTotal(json.multilateral_and_foundation_table);

    createBubbleGraph(json.five_largest_graph);

    fillSevenLargestDisbursementsTable(json.largest_disbursement_table.table);
    createSevenLargestDisbursementsGraph(json.largest_disbursement_table.graph);

    d3.select("#largest_other_text").text(json.summary.total_disbursements_count - 7);
}