var svg = d3.select("svg"),
  width = +svg.attr("width"),
  height = +svg.attr("height");

svg = svg
  .call(
    d3.zoom().on("zoom", () => {
      svg.attr("transform", d3.event.transform);
    })
  )
  .append("g");

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
  .force("center", d3.forceCenter(width / 2, height / 2))
  .force("x", d3.forceX())
  .force("y", d3.forceY());

d3.json("graph", function (error, graph) {
  if (error) throw error;

  var link = svg
    .append("g")
    .attr("class", "links")
    .selectAll("line")
    .data(graph.links)
    .enter()
    .append("line")
    .attr("stroke-width", 0.5);

  var node = svg
    .append("g")
    .attr("class", "nodes")
    .selectAll("g")
    .data(graph.nodes)
    .enter()
    .append("g");

  var circles = node
    .append("circle")
    .attr("r", 3)
    .attr("fill", function (d) {
      return color(d.group);
    })
    .on("click", (d) => {
      window.open(`/account/${d.id}`, "_blank");
    })
    .call(
      d3
        .drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended)
    );

  node.append("title").text(function (d) {
    return d.id + " - " + d.group;
  });

  simulation.nodes(graph.nodes).on("tick", ticked);

  simulation.force("link").links(graph.links);

  setTimeout(() => simulation.stop(), 60 * 1000);

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

    node.attr("transform", function (d) {
      return "translate(" + d.x + "," + d.y + ")";
    });
  }
});

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
