
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

function load_back(json) {
    /*********** Country Name ************/
    var country_name = d3.select("#countryname").text(json.country.name.toUpperCase());
    d3.select("#summary_amount").text(r2(json.summary.total_disbursements_sum));
    d3.select("#summary_count").text(r0(json.summary.total_disbursements_count));

    fillTable("#col", json.bilateral_table);
    fillTable("#mcol", json.multilateral_and_foundation_table);
    fillBilateralTotal(json.bilateral_table);
    fillMultilateralAndFoundationTotal(json.multilateral_and_foundation_table);

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