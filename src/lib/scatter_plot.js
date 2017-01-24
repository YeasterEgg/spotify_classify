import * as d3 from "d3"

const drawChart = (chartSelector, optionsSelector) => {
  let chart = d3.select(".chartSvg")
  let variables = document.variables["data"]

  let radius = 10 / Math.log10(Object.keys(variables).length)

  let variableX = d3.select(optionsSelector[0]).property("value")
  let variableY = d3.select(optionsSelector[1]).property("value")

  let yScale = d3.scaleLinear().domain([0, 1]).range([chart.node().height.baseVal.value, 0])
  let xScale = d3.scaleLinear().domain([0, 1]).range([chart.node().width.baseVal.value, 0])

  if(chart.selectAll("circle").size() == 0){
    chart.selectAll("circle")
         .data(variables, (d) => { return d.spotify_id; })
         .enter()
         .append("circle")
         .attr("stroke-width", 3)
         .attr("id", (d) => { return "spo_" + d.spotify_id; })
         .attr("fill", "transparent")
         .attr("r", radius)
         .on("click", (d) => { outlier(d) })
         .on("mouseover", circleMouseOver)
         .on("mouseout", circleMouseOver)

    chart.selectAll("circle")
         .transition()
         .attr("cx", (d) => { return xScale(d["values"][variableX]); })
         .attr("cy", (d) => { return yScale(d["values"][variableY]); })
         .attr("stroke", (d) => { return d.mood == "sad" ? "red" : "blue"; })

  }else{
    chart.selectAll("circle")
         .data(variables, (d) => {return d.spotify_id;})
         .transition()
         .attr("cx", (d) => { return xScale(d["values"][variableX]); })
         .attr("cy", (d) => { return yScale(d["values"][variableY]); })
  }
}

const outlier = (point) => {
  let circle = d3.select("#spo_" + point.spotify_id)
  circle.attr("opacity") == "1" ? circle.attr("opacity", "0.2") : circle.attr("opacity", "1")
}

const circleMouseOver = (song) => {
  circle = d3.select("#spo_" + song.spotify_id)
  svg.append("text")
     .attr({
       id: "txt_" + song.spotify_id,
       x: () => { return xScale(circle.x) - 30; },
       y: () => { return yScale(circle.y) - 15; }
     })
     .text(function() {
       return song.spotify_id;
     })
}

const circleMouseOut = (song) => {
  d3.select("#txt_" + song.spotify_id).remove()
}

module.exports = {
  drawChart: drawChart
}
