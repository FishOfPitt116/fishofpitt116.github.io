var term = "2224_";
var code = "CS";
var preqs = new Map();
var completed = new Map();

var apply = document.getElementById("apply");
apply.addEventListener('click', () => {
  let t = document.getElementById("term-select").value;
  let c = document.getElementById("code-select").value;
  if (t == 'Spring') {
    term = '2224_';
  } else {
    term = '2221_';
  }
  code = c;
  var svg = d3.select("svg");
  svg.selectAll("*").remove();
  setGraph(term, code);
});

setGraph(term, code);

function setGraph(term, code) {
  var svg = d3.select("svg"),
    width = +svg.attr("width"),
    height = +svg.attr("height");

  svg = svg.call(d3.zoom().on("zoom", function () {
    svg.attr("transform", d3.event.transform)
  })).append("g");

  svg.append('defs').append('marker')
    .attr('id', 'arrowhead')
    .attr('viewBox', '-0 -5 10 10')
    .attr('refX', 13)
    .attr('refY', 0)
    .attr('orient', 'auto')
    .attr('markerWidth', 10)
    .attr('markerHeight', 10)
    .attr('xoverflow', 'visible')
    .append('svg:path')
    .attr('d', 'M 0,-5 L 10 ,0 L 0,5')
    .attr('fill', '#999')
    .style('stroke','none');

  var color = d3.scaleOrdinal(d3.schemeCategory20);

  var g = svg.append("g")
    .attr("class", "everything");
    
  var simulation = d3.forceSimulation()
      .force("link", d3.forceLink().id(function(d) { return d.id; }).distance(200))
      .force("charge", d3.forceManyBody().strength(-50))
      .force('y', d3.forceY().y(function(d) { return d.id / 4; }))
      // .force('x', d3.forceX().x(function(d) { return d.id / 4; }))
      // .force('x', d3.forceX().x(function(d) { return (d.id*16) % 800; }))
      .force("center", d3.forceCenter(width / 2, height / 2));

  d3.json("../json/" + term + code + ".json", function(error, graph) {
    console.log(graph.nodes);
    preqs = new Map();
    completed = new Map();
    for (node of graph.nodes) {
      preqs.set(node.id, node.prereq_count);
      completed.set(node.id, false);
    }
    console.log(preqs);
    if (error) throw error;

    var link = svg.append("g")
        .attr("class", "links")
      .selectAll("line")
      .data(graph.links)
      .enter().append("line")
      .attr("stroke-width", function(d) { return 3; })
      .attr('marker-end', 'url(#arrowhead)');

    var node = svg.append("g")
      .attr("class", "nodes")
      .selectAll("g")
      .data(graph.nodes)
      .enter().append("g");
      // .on('dblclick', function(d) { alert(d.id + " is the node you selected") });

    var circles = node.append("circle")
      .attr("r", 20)
      .attr("fill", function(d) { if (completed.get(d.id) == false) { if (preqs.get(d.id) == 0) { return 'yellow'; } else { return 'grey'; } } else { return 'lightgreen'; }} )
      .on("dblclick", function(d) {
        currentColor = d3.select(this).attr("fill")
        if (currentColor == "grey") {
          return;
        }
        currentColor = currentColor == "lightgreen" ? "yellow" : "lightgreen";
        d3.select(this).attr("fill", currentColor);
      })
      .on("contextmenu", function(d) {
        console.log("right click");
        d3.event.preventDefault();

        let body = document.body;
        let newDiv = document.createElement("div");
        newDiv.id = "alertDiv";

        let courseTitle = document.createElement("h1");
        courseTitle.textContent = d.dept_code + " " + d.id + " " + d.course_title;
        newDiv.appendChild(courseTitle);

        let description = document.createElement("p");
        description.textContent = d.description;
        newDiv.appendChild(description);

        let button = document.createElement("button");
        button.textContent = "Close";
        button.addEventListener('click', () => {
          body.removeChild(newDiv);
        });
        newDiv.appendChild(button);

        body.appendChild(newDiv);
      });
      // .attr("text", function(d) { return d.id });

    // Create a drag handler and append it to the node object instead
    var drag_handler = d3.drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended);

    drag_handler(node);
    
    var labels = node.append("text")
        .text(function(d) {
          return d.id;
        })
        .attr("text-anchor", "middle")
        // .attr("text-align", "center")
        .attr('x', 6)
        .attr('y', 3);

    node.append("title")
        .text(function(d) { return d.id; });

    simulation
        .nodes(graph.nodes)
        .on("tick", ticked);

    simulation.force("link")
        .links(graph.links);
    // if (graph.nodes == []) {
    //   svg.append("text")
    //   .text("No courses found for this term and subject. Refine your search criteria.")
    //   .attr("text-anchor", "middle")
    // }

    function ticked() {
      link
          .attr("x1", function(d) { return d.source.x; })
          .attr("y1", function(d) { return d.source.y; })
          .attr("x2", function(d) { return d.target.x; })
          .attr("y2", function(d) { return d.target.y; });

      node
          .attr("transform", function(d) {
            return "translate(" + d.x + "," + d.y + ")";
          })
    }

    // preqs = {};
    // for (link of graph.links) {
    //   if (preqs[link.source] == undefined) {
    //     preqs[link.source] = 0;
    //   }
    //   if (preqs[link.target] == undefined) {
    //     preqs[link.source] = 1;
    //   } else {
    //     preqs[link.source] += 1;
    //   }
    // }
    // console.log(preqs);
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
    d.x = validate(d.x, 0, width);
    d.y = validate(d.y, 0, height);
  }
  
  function validate(x, a, b) {
    if (x < a) x = a + 50;
    if (x > b) x = b - 50;
    return x;
  }
  
  //Zoom functions 
  function zoom_actions(){
      g.attr("transform", d3.event.transform)
  }

  function check_completed(d, node_id) {

  }
}