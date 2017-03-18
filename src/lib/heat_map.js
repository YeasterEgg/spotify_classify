const d3 = require('d3')

export class HeatMap{
  constructor(sizes, container, data){
    this.sizes       = sizes
    this.container   = container
    this.matrix      = data["cov"]
    this.headers     = data["headers"]["numeric"]
    this.chart       = null
    this.plot        = null
    this.variablesNo = data["cov"].length
    this.cellSizes   = {}
    this.colorScale  = d3.scaleLinear().domain([-1, 1]).range([-255, 255])
  }

  draw(scatterPlot){
    this.scatterPlot = scatterPlot
    this.computeCellSizes()
    this.chart = this.container
                     .append("g")
                     .attr("class", "charts-heatMap_container")
                     .style("opacity", 0)
    this.drawAxis()
    this.drawCells()
    this.chart
        .transition()
        .duration(500)
        .style("opacity", 1)
  }

  valueToColor(value){
    return value >= 0 ? this.blueCell(value) : this.redCell(value)
  }

  redCell(value){
    const others = ("00" + (255 + Math.ceil(value)).toString(16)).slice(-2)
    return "#ff" + others + others
  }

  blueCell(value){
    const others = ("00" + (255 - Math.ceil(value)).toString(16)).slice(-2)
    return "#" + others + others + "ff"
  }

  computeCellSizes(){
    this.cellSizes["cellWidthPx"]  = this.sizes.chartWidth / this.variablesNo
    this.cellSizes["cellHeightPx"] = this.sizes.chartHeight / this.variablesNo
    this.cellSizes["xAxisLength"]  = this.sizes.chartWidth
    this.cellSizes["xAxisMargin"]  = this.sizes.chartWidth / this.variablesNo - this.cellSizes.cellWidthPx
    this.cellSizes["yAxisLength"]  = this.sizes.chartHeight + this.cellSizes.cellHeightPx
    this.cellSizes["yAxisMargin"]  = this.sizes.chartHeight / this.variablesNo
  }

  drawCells(){
    this.plot = this.chart
                    .append("g")
                    .attr("class", "charts-heatMap_plot")
    this.matrix.map((variable, idx) => {
      const otherIdx = this.variablesNo - 1 - idx
      const group = this.plot
                        .append("g")
                        .selectAll("rect")
                        .data(variable)
                        .enter()
                        .append("g")
                        .attr("id", (d, i) => {return "r_" + otherIdx + "_" + i})

      group.on("mouseover", (d, i) => {this.mouseOverHandler(otherIdx, i)} )
      group.on("mouseout", (d, i) => {this.mouseOutHandler(otherIdx, i)} )
      group.on("click", (d, i) => {this.clickHandler(otherIdx, i)} )

      group.append("rect")
           .attr("x", (d,i) => {return this.cellSizes.cellWidthPx * i + this.sizes.marginLeft + 1})
           .attr("y", (d,i) => {return this.cellSizes.cellHeightPx * otherIdx + this.sizes.marginTop})
           .attr("rx", 5)
           .attr("ry", 5)
           .attr("width", this.cellSizes.cellWidthPx)
           .attr("height", this.cellSizes.cellHeightPx)
           .attr("fill", (d) => {return this.valueToColor(this.colorScale(d))})

      group.append("text")
           .attr("x", (d,i) => {return this.cellSizes.cellWidthPx * (i + 0.5) + this.sizes.marginLeft + 1})
           .attr("y", (d,i) => {return this.cellSizes.cellHeightPx * (otherIdx + 0.5) + this.sizes.marginTop})
           .attr("width", this.cellSizes.cellWidthPx)
           .attr("height", this.cellSizes.cellHeightPx)
           .attr("text-anchor", "middle")
           .attr("alignment-baseline", "central")
           .attr("font-size", "80%")
           .attr("font-family", "Arial, Helvetica, sans-serif")
           .text((d) => {return Math.round(d * 1000) / 1000})
    })
  }

  drawAxis(){
    const xHeaders = this.headers.concat([""])
    const yHeaders = [""].concat(this.headers)
    yHeaders.reverse()
    const xScale = d3.scalePoint()
                     .domain(xHeaders)
                     .range([this.cellSizes.xAxisMargin , this.cellSizes.xAxisLength])
    const yScale = d3.scalePoint()
                     .domain(yHeaders)
                     .range([this.cellSizes.yAxisMargin , this.cellSizes.yAxisLength])
    const xAxis = d3.axisBottom(xScale)
    const yAxis = d3.axisLeft(yScale)

    this.chart
        .append("g")
        .attr("class", "x_axis")
        .attr("transform", "translate(" + this.sizes.marginLeft + "," + (this.sizes.marginTop + this.sizes.chartHeight) + ")")
        .call(xAxis)
        .selectAll("text")
        .attr("x", -this.cellSizes.cellWidthPx / 2 + "px")
        .attr("y", this.cellSizes.cellHeightPx / 2 + "px")
        .attr("transform", "rotate(-70)")
        .attr("font-family", "Arial, Helvetica, sans-serif")

    this.chart
        .append("g")
        .attr("class", "y_axis")
        .attr("transform", "translate(" + this.sizes.marginLeft + "," + (this.sizes.marginTop - this.cellSizes.cellHeightPx) + ")")
        .call(yAxis)
        .selectAll("text")
        .attr("y", this.cellSizes.cellHeightPx / 2 + "px")
        .attr("transform", "rotate(-20)")
        .attr("font-family", "Arial, Helvetica, sans-serif")
  }

  mouseOverHandler(variable1Idx, variable2Idx){
    d3.select("#r_" + variable1Idx + "_" + variable2Idx)
      .attr("opacity", 0.5)
  }

  mouseOutHandler(variable1Idx, variable2Idx){
    d3.select("#r_" + variable1Idx + "_" + variable2Idx)
      .attr("opacity", 1)
  }

  clickHandler(variable1Idx, variable2Idx){
    this.scatterPlot.fill(variable1Idx, variable2Idx)
  }

  hide(){
    this.chart
        .transition()
        .duration(500)
        .style("opacity", 0)
        .on("end", () => {
          this.chart.style("display", "none")
        })
  }

  show(){
    this.chart
        .style("display", "block")
        .transition()
        .duration(500)
        .style("opacity", 1)
  }
}
