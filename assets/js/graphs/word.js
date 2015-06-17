var r = 8;
var width = $("#graph").width(), height = window.innerHeight - 220;
var fill = d3.scale.category20();

d3.json(url, function(data) {
    var linkedByIndex = {};
    for (i = 0; i < data.nodes.length; i++) { linkedByIndex[i + "," + i] = 1; };
    data.links.forEach(function (d) { linkedByIndex[d.source + "," + d.target] = 1; });

    var force = d3.layout.force()
            .nodes(d3.values(data.nodes))
            .links(data.links)
            .size([width, height])
            .linkDistance(150)
            .distance(150)
            .charge(-150)
            .on("tick", tick)
            .start();
    var svg = d3.select("#graph").append("svg:svg")
            .attr("width", width)
            .attr("height", height);

    var link = svg.selectAll("g.link")
            .data(data.links)
            .enter().append("svg:line")
            .attr("class", "link")
            .style("stroke-width", function(d) { return Math.sqrt(d.value); });

    var node_drag = d3.behavior.drag()
            .on("dragstart", dragstart)
            .on("drag", dragmove)
            .on("dragend", dragend);

    var node = svg.selectAll("g.node")
            .data(data.nodes)
            .enter().append("svg:g")
            .attr("class", "node")
            .style("fill", function(d) { return fill(d.group); })
            .on("mouseover", mouseover)
            .on("mouseout", mouseout)
            .call(node_drag)
            .on('dblclick', releaseNode);
    node.append("circle")
            .attr("class", "node")
            .attr("r", r);
    node.append("svg:title")
            .text(function(d) { return d.name; });
    node.append("svg:text")
            .attr("x", 12)
            .attr("dy", ".35em")
            .style("fill",function(d) { return fill(d.group); })
            .append("a")
            .attr("xlink:href", function (d) { return "/words/" + d.id; } )
            .text(function(d) { return d.name; });

    function tick() {
        link.attr("x1", function(d) { return d.source.x; })
                .attr("y1", function(d) { return d.source.y; })
                .attr("x2", function(d) { return d.target.x; })
                .attr("y2", function(d) { return d.target.y; });
        node.attr("transform", function(d) { return "translate(" + Math.max(r, Math.min(width - r, d.x)) + "," + Math.max(r, Math.min(height - r, d.y)) + ")"; });
    }

    function mouseover() {
        d3.select(this).select("circle").transition()
                .duration(750)
                .attr("r", 16);
        d3.select(this).select("text").transition()
                .duration(750)
                .attr("x", 20)
                .style("font-size", "14px");

        d = d3.select(this).node().__data__;
        node.transition().duration(750).style("opacity", function (o) {
            return neighboring(d, o) | neighboring(o, d) ? 1 : 0.1;
        });
        link.transition().duration(750).style("opacity", function (o) {
            return d.index===o.source.index | d.index===o.target.index ? 1 : 0.1;
        });
    }

    function mouseout() {
        d3.select(this).select("circle").transition()
                .duration(750)
                .attr("r", r);
        d3.select(this).select("text").transition()
                .duration(750)
                .attr("x", 12)
                .style("font-size", "10px");
        node.transition().duration(750).style("opacity", 1);
        link.transition().duration(750).style("opacity", 1);
    }

    function neighboring(a, b) { return linkedByIndex[a.index + "," + b.index]; }
    function releaseNode(d) { d.fixed = false; }
    function dragstart(d, i) { force.stop(); }
    function dragmove(d, i) {
        d.px += d3.event.dx;
        d.py += d3.event.dy;
        d.x += d3.event.dx;
        d.y += d3.event.dy;
        tick();
    }

    function dragend(d, i) {
        d.fixed = true;
        force.resume();
    }
})