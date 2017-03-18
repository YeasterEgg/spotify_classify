const d3 = require('d3')

export class ScatterPlot{
  constructor(sizes, container, data){
    this.sizes       = sizes
    this.container   = container
    this.data        = data
    this.chart       = null
    this.plot        = null
    this.variablesNo = data["cov"].length
    this.headers     = data["headers"]
    this.cellSizes   = {}
    this.colorScale  = d3.scaleLinear().domain([-1, 1]).range([-255, 255])
    this.variables   = data["data"]
  }

  draw(heatMap, radialPlot){
    this.heatMap = heatMap
    this.radialPlot = radialPlot
    this.drawTooltip()
    this.drawAxis()
    this.drawChart()
  }

  drawChart(){
    this.chart = this.container
                     .append("g")
                     .attr("class", "charts-scatterplot_container")
                     .style("opacity", 0)
                     .attr("transform", "translate(" + (this.sizes.w/2) + ",0)")

    this.plot = this.chart.append("g")

    this.plot
        .attr("id", "heatmap_plot")
        .attr("width", this.sizes.chartWidth + "px")
        .attr("height", this.sizes.chartHeight + "px")
        .attr("x", this.sizes.chartWidth + this.sizes.marginLeft + "px")
        .attr("y", this.sizes.marginTop + "px")

    this.circles = this.plot
                       .selectAll("circle")
                       .data(this.variables, (d) => { return d.spotify_id + d.mood; })
                       .enter()
                       .append("circle")
                       .attr("fill", "transparent")
                       .attr("stroke-width", 5)
                       .attr("stroke", (d) => { return d.mood == "sad" ? "red" : "blue" })

    this.circles.on("click", (d) => { this.onClick(d) })
    this.circles.on("mouseover", (d) => { this.showTooltip(d) })
    this.circles.on("mouseout", (d) => { this.hideTooltip() })

    this.chart
        .append("g")
        .attr("class", "x_axis")
        .attr("transform", "translate(" + this.sizes.marginLeft + "," + (this.sizes.marginTop + this.sizes.chartHeight) + ")")
        .call(this.xAxis)

    this.chart
        .append("g")
        .attr("class", "y_axis")
        .attr("transform", "translate(" + this.sizes.marginLeft + "," + this.sizes.marginTop + ")")
        .call(this.yAxis)

    this.chart
        .append("text")
        .attr("class", "x_axis_title")
        .attr("text-anchor", "middle")
        .attr("font-family", "Arial, Helvetica, sans-serif")
        .attr("transform", "translate(" + (this.sizes.marginLeft + this.sizes.chartWidth / 2) + "," + (this.sizes.marginTop + this.sizes.chartHeight + this.sizes.marginBottom / 2) + ")")
        .text("Variable X")

    this.chart
        .append("text")
        .attr("class", "y_axis_title")
        .attr("text-anchor", "middle")
        .attr("font-family", "Arial, Helvetica, sans-serif")
        .attr("transform", "translate(" + (this.sizes.marginLeft / 2) + "," + (this.sizes.marginTop + this.sizes.chartHeight / 2) + ") rotate(-90)")
        .text("Variable Y")

    this.chart
        .transition()
        .duration(500)
        .style("opacity", 1)
  }

  drawAxis(){
    const yAxisScale = d3.scaleLinear().domain([0, 1]).range([this.sizes.chartHeight, 0])
    const xAxisScale = d3.scaleLinear().domain([0, 1]).range([this.sizes.chartWidth, 0])
    this.radius = 20 / Math.log10(this.variables.length)
    this.yValueScale = d3.scaleLinear().domain([0, 1]).range([this.sizes.chartHeight - this.radius, this.radius])
    this.xValueScale = d3.scaleLinear().domain([0, 1]).range([this.sizes.chartWidth - this.radius, this.radius])
    this.xAxis = d3.axisBottom(xAxisScale)
    this.yAxis = d3.axisLeft(yAxisScale)
  }

  drawTooltip(){
    this.tooltip = d3.select("body")
                     .append("div")
                     .attr("class", "scatter_tooltip tooltip")
                     .style("opacity", 0);
  }

  fill(xVariableIndex, yVariableIndex){
    const variableX = this.headers.numeric[xVariableIndex]
    const variableY = this.headers.numeric[yVariableIndex]
    this.variables = this.data["data"]
    this.plot
        .selectAll("circle")
        .data(this.variables, (d) => {return d.spotify_id + d.mood;})
        .transition()
        .attr("cx", (d) => { return this.xValueScale(d["values"][variableX]) + this.sizes.marginLeft})
        .attr("cy", (d) => { return this.yValueScale(d["values"][variableY]) + this.sizes.marginTop})
        .attr("r", this.radius)

    d3.select(".x_axis_title")
      .text(variableX)

    d3.select(".y_axis_title")
      .text(variableY)
  }

  showTooltip(d){
    this.tooltip.transition()
                .duration(300)
                .style("opacity", 0.9)

    this.tooltip.html("<span class='title'>" + d.title + "</span><span class='artist'>" + d.artist + "</span>")
                .style("right", (this.sizes.w - d3.event.pageX) + "px")
                .style("top", (d3.event.pageY - 30) + "px")
  }

  hideTooltip(){
    this.tooltip.transition()
                .duration(300)
                .style("opacity", 0)
  }

  onClick(d){
    this.heatMap.hide()
    this.radialPlot.fill(d)
  }

}

