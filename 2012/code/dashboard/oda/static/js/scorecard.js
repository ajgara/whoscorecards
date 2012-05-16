// Add a startWith method to strings
if (typeof String.prototype.startsWith != 'function') {
  String.prototype.startsWith = function (str){
    return this.indexOf(str) == 0;
  };
}

if (typeof Number.prototype.formatThousands != 'function') {
    Number.prototype.formatThousands = function(c, d, t) {
        var n = this, c = isNaN(c = Math.abs(c)) ? 2 : c, d = d == undefined ? "." : d, t = t == undefined ? "," : t, s = n < 0 ? "-" : "", i = parseInt(n = Math.abs(+n || 0).toFixed(c)) + "", j = (j = i.length) > 3 ? j % 3 : 0;
       return s + (j ? i.substr(0, j) + t : "") + i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + t) + (c ? d + Math.abs(n - i).toFixed(c).slice(2) : "");
    }
}

r0 = function(v) { return v.formatThousands(0); }
r1 = function(v) { return v.formatThousands(1); }
r2 = function(v) { return v.formatThousands(2); }


function load_front(json) {
    var country_name = d3.select("#countryname").text(json.country.name.toUpperCase());
    d3.select("#sum_increase").text(r1(json.summary.sum_increase) + "%");
    d3.select("#sum_amount").text(r0(json.summary.sum_amount) + "%");
    d3.select("#sum_2000").text(r0(json.summary.sum_2000) + "%");

    var all_years = ["2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010"];
    _.each(all_years, function(el, i) {
        var indicators = json.indicators[el];
        d3.select("#indc" + (i + 2) + "r1").text(r1(indicators["Population as at 30 june of each year"] / 1000000));
        d3.select("#indc" + (i + 2) + "r2").text(r2(indicators["Commitments TOTAL ODA  (Million constant 2009 US$)"]));
        d3.select("#indc" + (i + 2) + "r3").text(r2(indicators["Disbursements TOTAL ODA  (Million constant 2009 US$)"]));
        d3.select("#indc" + (i + 2) + "r4").text(r2(indicators["ODA for Health Commitments, (Million constant 2009 US$)"]));
        d3.select("#indc" + (i + 2) + "r5").text(r2(indicators["ODA for Health Disbursements (Million constant 2009 US$)"]));
        d3.select("#indc" + (i + 2) + "r6").text(r2(indicators["Commitments: Ratio Health / Total ODA"]));
        d3.select("#indc" + (i + 2) + "r7").text(r2(indicators["Disbursements:  Ratio Health / Total ODA"]));
        d3.select("#indc" + (i + 2) + "r8").text(r2(indicators["Commitments per capita USD"]));
        d3.select("#indc" + (i + 2) + "r9").text(r2(indicators["Disbursements per capita USD"]));
        d3.select("#indc" + (i + 2) + "r10").text(r2(indicators["Regional AvComm per capita"]));
        d3.select("#indc" + (i + 2) + "r11").text(r2(indicators["Regional AvDisb per capita"]));
        d3.select("#indc" + (i + 2) + "r12").text(r2(indicators["Total expenditure on health (curr US$ p.c.)"]));
        d3.select("#indc" + (i + 2) + "r13").text(r2(indicators["General government expenditure on health (curr US$ p.c.)"]));
        d3.select("#indc" + (i + 2) + "r14").text(r2(indicators["Private expenditure on health (curr US$ p.c.)"]));


        var allocation_commitments = json.allocations.commitments[el];
        var allocation_disbursements = json.allocations.disbursements[el];
        d3.select("#allcc" + (i + 1) + "r1").text(r2(allocation_commitments["HEALTH POLICY & ADMIN. MANAGEMENT"]));
        d3.select("#allcc" + (i + 1) + "r2").text(r2(allocation_commitments["MDG6"]));
        d3.select("#allcc" + (i + 1) + "r3").text(r2(allocation_commitments["Other Health Purposes"]));
        d3.select("#allcc" + (i + 1) + "r4").text(r2(allocation_commitments["RH & FP"]));
        d3.select("#allcc" + (i + 1) + "r5").text(r2(
              allocation_commitments["HEALTH POLICY & ADMIN. MANAGEMENT"]
            + allocation_commitments["MDG6"]
            + allocation_commitments["Other Health Purposes"]
            + allocation_commitments["RH & FP"]
        ));

        d3.select("#alldc" + (i + 1) + "r1").text(r2(allocation_disbursements["HEALTH POLICY & ADMIN. MANAGEMENT"]));
        d3.select("#alldc" + (i + 1) + "r2").text(r2(allocation_disbursements["MDG6"]));
        d3.select("#alldc" + (i + 1) + "r3").text(r2(allocation_disbursements["Other Health Purposes"]));
        d3.select("#alldc" + (i + 1) + "r4").text(r2(allocation_disbursements["RH & FP"]));
        d3.select("#alldc" + (i + 1) + "r5").text(r2(
              allocation_disbursements["HEALTH POLICY & ADMIN. MANAGEMENT"]
            + allocation_disbursements["MDG6"]
            + allocation_disbursements["Other Health Purposes"]
            + allocation_disbursements["RH & FP"]
        ));

        // segment pie
        var segpie = {
            width: 31,
            height:31,
            node : "#allc_pie" + (2000 + i),

            arc: {
                margin: 25,
                width: 15,
            },
            data : [
                {"value" : allocation_disbursements["HEALTH POLICY & ADMIN. MANAGEMENT"]},
                {"value" : allocation_disbursements["MDG6"]},
                {"value" : allocation_disbursements["Other Health Purposes"]},
                {"value" : allocation_disbursements["RH & FP"]}
            ],
            colors : ["#cf3e96", "#62A73B", "#79317F", "#009983"],
        };
        
        var segpiegraph = new SegmentPieGraph(segpie);

        
    });

    /*
    // bar charts
    var rounded = {
        bar: {
            'margin' : 4, // pixels between bars
            'width': 185, // width of bars
            'rounding': 3, // pixels for rounding effect
            'color': '#0093d5'
        },

        line: {
            const_val: '0'
        },
        node: "#bargraph1",
        width : 170,
        height : 93,
        data : _.reduce(all_years, function(memo, year) {
            indicator = json.indicators[year]["ODA for Health Commitments, (Million constant 2009 US$)"];
            memo.push({"value" : indicator, "series" : year});
            return memo;
        }, []);
    }
    rbg = new RoundedBarGraph(ctx)
    */
}
function load_back(json) {
    /*********** Country Name ************/
    var country_name = d3.select("#countryname").text(json.country.name.toUpperCase());
    d3.select("#summary_amount").text(r2(json.summary.total_disbursements_sum) + "M");
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
    var num = 32432432423;
    console.log(num.formatThousands());    

}
