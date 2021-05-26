var svg = d3.select("svg");
var width = +svg.attr("width");
var height = +svg.attr("height");

svg.attr("viewBox", [-width / 2, -height / 2, width, height]);

var g = svg.append("g");

var color = d3.scaleOrdinal(d3.schemeCategory10);

var simulation = d3
  .forceSimulation()
  .force(
    "link",
    d3.forceLink().id(function (d) {
      return d.id;
    })
  )
  .force("charge", d3.forceManyBody())
  .force("x", d3.forceX())
  .force("y", d3.forceY());

d3.json("graph", function (error, graph) {
  if (error) throw error;

  var link = g
    .append("g")
    .attr("class", "links")
    .selectAll("line")
    .data(graph.links)
    .enter()
    .append("line");

  var node = g
    .append("g")
    .attr("class", "nodes")
    .selectAll("circle")
    .data(graph.nodes)
    .enter()
    .append("circle")
    .attr("r", 5)
    .attr("fill", function (d) {
      return color(d.group);
    })
    .on("dblclick", function (d) {
      window.open("/account/" + d.id, "_blank");
    })
    .call(
      d3
        .drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended)
    );

  svg.call(d3.zoom().on("zoom", zoomed));

  node.append("title").text(function (d) {
    return d.id + " - " + d.group;
  });

  simulation.nodes(graph.nodes).on("tick", ticked);

  simulation.force("link").links(graph.links);

  function ticked() {
    link
      .attr("x1", function (d) {
        return d.source.x;
      })
      .attr("y1", function (d) {
        return d.source.y;
      })
      .attr("x2", function (d) {
        return d.target.x;
      })
      .attr("y2", function (d) {
        return d.target.y;
      });

    node
      .attr("cx", function (d) {
        return d.x;
      })
      .attr("cy", function (d) {
        return d.y;
      });
  }
});

function zoomed() {
  let e = d3.event;

  if (e.transform.k > 2 && lastK != e.transform.k) {
    lastK = e.transform.k;
    console.log("zoomed");
    zoomLvl = Math.log2(e.transform.k);
    globalNode.attr("stroke-width", 1.5 / zoomLvl);
    link.attr("stroke-width", (d) => Math.sqrt(d.value) / zoomLvl);
  }

  g.attr("transform", e.transform);
}

function dragstarted(d) {
  if (!d3.event.active) simulation.alphaTarget(0.3).restart();
  d.fx = d.x;
  d.fy = d.y;
}

function dragged(d) {
  d.fx = d3.event.x;
  d.fy = d3.event.y;
}

function dragended(d) {
  if (!d3.event.active) simulation.alphaTarget(0);
  d.fx = null;
  d.fy = null;
}
