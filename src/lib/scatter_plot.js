const d3 = require('d3')
const fillRadial =  require('./radial_plot.js').fillRadial

let plot = {
  plot: null,
  xAxisScale: null,
  xValueScale: null,
  yAxisScale: null,
  yValueScale: null,
  sizes: null
}

export const drawScatter = () => {
  document.world.scatterPlot = document.world
                                       .container
                                       .append("g")
                                       .attr("class", "charts-scatterplot_container")
                                       .style("opacity", 0)
                                       .attr("transform", "translate(" + (document.world.w/2) + ",0)")

  plot.yAxisScale = d3.scaleLinear().domain([0, 1]).range([document.world.sizes.chartHeight, 0])
  plot.xAxisScale = d3.scaleLinear().domain([0, 1]).range([document.world.sizes.chartWidth, 0])
  const variables = document.world.data["data"]
  const radius = 10 / Math.log10(variables.length)

  plot.yValueScale = d3.scaleLinear().domain([0, 1]).range([document.world.sizes.chartHeight - radius, radius])
  plot.xValueScale = d3.scaleLinear().domain([0, 1]).range([document.world.sizes.chartWidth - radius, radius])
  const xAxis = d3.axisBottom(plot.xAxisScale)
  const yAxis = d3.axisLeft(plot.yAxisScale)

  plot.plot = document.world.scatterPlot.append("g")

  plot.plot
      .attr("id", "heatmap_plot")
      .attr("width", document.world.sizes.chartWidth + "px")
      .attr("height", document.world.sizes.chartHeight + "px")
      .attr("x", document.world.sizes.chartWidth + document.world.sizes.marginLeft + "px")
      .attr("y", document.world.sizes.marginTop + "px")

  plot.plot
      .selectAll("circle")
      .data(variables, (d) => { return d.spotify_id + d.mood; })
      .enter()
      .append("circle")
      .attr("fill", "transparent")
      .attr("stroke-width", 3)
      .attr("stroke", (d) => { return d.mood == "sad" ? "red" : "blue" })
      .on("click", (d) => { fillRadial(d) })

  document.world
          .scatterPlot
          .append("g")
          .attr("class", "x_axis")
          .attr("transform", "translate(" + document.world.sizes.marginLeft + "," + (document.world.sizes.marginTop + document.world.sizes.chartHeight) + ")")
          .call(xAxis)

  document.world
          .scatterPlot
          .append("g")
          .attr("class", "y_axis")
          .attr("transform", "translate(" + document.world.sizes.marginLeft + "," + document.world.sizes.marginTop + ")")
          .call(yAxis)

  document.world
          .scatterPlot
          .append("text")
          .attr("class", "x_axis_title")
          .attr("text-anchor", "middle")
          .attr("font-family", "Arial, Helvetica, sans-serif")
          .attr("transform", "translate(" + (document.world.sizes.marginLeft + document.world.sizes.chartWidth / 2) + "," + (document.world.sizes.marginTop + document.world.sizes.chartHeight + document.world.sizes.marginBottom / 2) + ")")
          .text("Variable X")

  document.world
          .scatterPlot
          .append("text")
          .attr("class", "y_axis_title")
          .attr("text-anchor", "middle")
          .attr("font-family", "Arial, Helvetica, sans-serif")
          .attr("transform", "translate(" + (document.world.sizes.marginLeft / 2) + "," + (document.world.sizes.marginTop + document.world.sizes.chartHeight / 2) + ") rotate(-90)")
          .text("Variable Y")

  document.world
          .scatterPlot
          .transition()
          .duration(500)
          .style("opacity", 1)
}

export const fillScatter = (xVariableIndex, yVariableIndex) => {
  const variableX = document.world.data.headers.numeric[xVariableIndex]
  const variableY = document.world.data.headers.numeric[yVariableIndex]
  const variables = document.world.data["data"]

  const radius = 10 / Math.log10(variables.length)

  plot.plot
      .selectAll("circle")
      .data(variables, (d) => {return d.spotify_id + d.mood;})
      .transition()
      .attr("cx", (d) => { return plot.xValueScale(d["values"][variableX]) + document.world.sizes.marginLeft})
      .attr("cy", (d) => { return plot.yValueScale(d["values"][variableY]) + document.world.sizes.marginTop})
      .attr("r", radius)

  d3.select(".x_axis_title")
    .text(variableX)

  d3.select(".y_axis_title")
    .text(variableY)
}
