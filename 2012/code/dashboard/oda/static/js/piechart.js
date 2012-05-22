/*
Adapted from https://gist.github.com/1203641
*/
Piechart = function(ctx){
    if (ctx.width === undefined){ throw Error('No width given.'); }
    this.w = ctx.width;

    if (ctx.height === undefined){ throw Error('No height given.'); }
    this.h = ctx.height;

    if (ctx.radius === undefined){ throw Error('No radius given.'); }
    this.r = ctx.radius;

    if (ctx.node === undefined){ throw Error('No Node given'); }
    //this.node =  d3.select(ctx.node);
    this.node =  ctx.node;

    this.color = ctx.colors || d3.scale.category20c();     //builtin range of colors

    if (ctx.data !== undefined && ctx.data !== null){
        this.update_data(ctx.data);
    }

    /*
    data = [{"label":"one", "value":20}, 
            {"label":"two", "value":50}, 
            {"label":"three", "value":30}];
    */
}

Piechart.prototype = {
    
    update_data : function(data) {
        if (data.length === undefined || data.length === 0) { return; }
        var me = this;

        this.vis = d3.select(this.node).append("svg")
            .attr("class", "piechart")
            .attr("width", this.w)
            .attr("height", this.h)
            .append('g')
            .attr("transform", "translate(" + (this.r) + "," + (this.r) + ")");

        var arc = d3.svg.arc()              //this will create <path> elements for us using arc data
            .outerRadius(this.r);

        var pie = d3.layout.pie()           //this will create arc data for us given a list of values
            .value(function(d) { return d.value; });    //we must tell it out to access the value of each element in our data array

        var arcs = this.vis.selectAll("g.slice")     //this selects all <g> elements with class slice (there aren't any yet)
            .data(pie)                          //associate the generated pie data (an array of arcs, each having startAngle, endAngle and value properties) 
            .enter()                            //this will create <g> elements for every "extra" data element that should be associated with a selection. The result is creating a <g> for every object in the data array
            .append("svg:g")                //create a group to hold each slice (we will have a <path> and a <text> element associated with each slice)
            .attr("class", "slice");    //allow us to style things in the slices (like text)

        arcs.append("svg:path")
            .attr("fill", function(d, i) { return me.color(i); } ) //set the color for each slice to be chosen from the color function defined above
            .attr("d", arc);                                    //this creates the actual SVG path using the associated data (pie) with the arc drawing function

        arcs.append("svg:text")                                     //add a label to each slice
            .attr("transform", function(d) {                    //set the label's origin to the center of the arc
                //we have to make sure to set these before calling arc.centroid
                d.innerRadius = 0;
                d.outerRadius = this.r;
                return "translate(" + arc.centroid(d) + ")";        //this gives us a pair of coordinates like [50, 50]
            })
            .attr("text-anchor", "middle")                          //center the text on it's origin
            .text(function(d, i) { return data[i].label; });        //get the label from our original data array
    }
};
        
