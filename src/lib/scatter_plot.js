import * as d3 from "d3"

const drawChart = (xVariableIndex, yVariableIndex, chart) => {
  const sizes = document.chartSizes
  const variableX = document.variables.headers.numeric[xVariableIndex]
  const variableY = document.variables.headers.numeric[yVariableIndex]
  const variables = document.variables["data"]
  const radius = 10 / Math.log10(variables.length)
  const yScale = d3.scaleLinear().domain([0, 1]).range([sizes.height, 0])
  const xScale = d3.scaleLinear().domain([0, 1]).range([sizes.width, 0])
  const xAxis = d3.axisBottom(xScale)
  const yAxis = d3.axisLeft(yScale)

  const plot = do {
    if(chart.selectAll("g").size() == 0){
      chart.append("g")
           .append("svg")
    }else{
      chart.selectAll("g")
           .selectAll("svg")
    }
  }

  plot.attr("id", "heatmap_plot")
      .attr("width", sizes.width + "px")
      .attr("height", sizes.height + "px")
      .attr("x", sizes.marginLeft + "px")
      .attr("y", sizes.marginTop + "px")

  if(plot.selectAll("circle").size() == 0){
    plot.selectAll("circle")
        .data(variables, (d) => { return d.spotify_id + d.mood; })
        .enter()
        .append("circle")
        .attr("stroke-width", 3)
        .attr("id", (d) => { return "spo_" + d.spotify_id; })
        .attr("fill", "transparent")
        .attr("r", radius)

    plot.selectAll("circle")
        .transition()
        .attr("cx", (d) => { return xScale(d["values"][variableX]); })
        .attr("cy", (d) => { return yScale(d["values"][variableY]); })
        .attr("stroke", (d) => { return d.mood == "sad" ? "red" : "blue"; })
  }else{
    plot.selectAll("circle")
        .data(variables, (d) => {return d.spotify_id + d.mood;})
        .transition()
        .attr("cx", (d) => { return xScale(d["values"][variableX]); })
        .attr("cy", (d) => { return yScale(d["values"][variableY]); })
  }

  chart.append("g")
       .attr("class", "x axis")
       .attr("transform", "translate(" + sizes.marginLeft + "," + (sizes.marginTop + sizes.height) + ")")
       .call(xAxis)

  chart.append("g")
       .attr("class", "y axis")
       .attr("transform", "translate(" + sizes.marginLeft + "," + sizes.marginTop + ")")
       .call(yAxis)

}

module.exports = {
  drawChart: drawChart
}
