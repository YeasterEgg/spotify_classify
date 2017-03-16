const d3 = require('d3')
const fillScatter =  require('./scatter_plot.js').fillScatter

const valueToColor = (value) => {
  let others
  if(value >= 0){
    others = ("00" + (255 - Math.ceil(value)).toString(16)).slice(-2)
    return "#" + others + others + "ff"
  }else{
    others = ("00" + (255 + Math.ceil(value)).toString(16)).slice(-2)
    return "#ff" + others + others
  }
}

export const drawHeatMap = () => {
  document.world.heatMap = document.world
                                   .container
                                   .append("g")
                                   .attr("class", "charts-heatMap_container")
                                   .style("opacity", 0)

  const matrix = document.world.data["cov"]
  const headers = document.world.data["headers"]["numeric"]
  const variablesNo = matrix.length
  const cellSizes = computeCellSizes(variablesNo)
  drawAxis(headers, cellSizes)
  drawCells(matrix, cellSizes, variablesNo)
  document.world
          .heatMap
          .transition()
          .duration(500)
          .style("opacity", 1)
}

const computeCellSizes = (variablesNo) => {
  const cellSizes = {}
  cellSizes["cellWidthPx"]  = document.world.sizes.chartWidth / variablesNo
  cellSizes["cellHeightPx"] = document.world.sizes.chartHeight / variablesNo
  cellSizes["xAxisLength"]  = document.world.sizes.chartWidth
  cellSizes["xAxisMargin"]  = document.world.sizes.chartWidth / variablesNo - cellSizes.cellWidthPx
  cellSizes["yAxisLength"]  = document.world.sizes.chartHeight + cellSizes.cellHeightPx
  cellSizes["yAxisMargin"]  = document.world.sizes.chartHeight / variablesNo
  return cellSizes
}

const drawCells = (matrix, cellSizes, variablesNo) => {
  const plot = document.world
                       .heatMap
                       .append("g")
                       .attr("class", "charts-heatMap_plot")
  const colorScale = d3.scaleLinear().domain([-1, 1]).range([-255, 255])

  matrix.map((variable, idx) => {
    const otherIdx = variablesNo - 1 - idx
    const group = plot.append("g")
                      .selectAll("rect")
                      .data(variable)
                      .enter()
                      .append("g")
                      .attr("id", (d, i) => {return "r_" + otherIdx + "_" + i})

    group.on("mouseover", (d, i) => {mouseOverHandler(d, otherIdx, i)} )
    group.on("mouseout", (d, i) => {mouseOutHandler(d, otherIdx, i)} )
    group.on("click", (d, i) => {clickHandler(otherIdx, i)} )

    group.append("rect")
         .attr("x", (d,i) => {return cellSizes.cellWidthPx * i + document.world.sizes.marginLeft + 1})
         .attr("y", (d,i) => {return cellSizes.cellHeightPx * otherIdx + document.world.sizes.marginTop})
         .attr("rx", 5)
         .attr("ry", 5)
         .attr("width", cellSizes.cellWidthPx)
         .attr("height", cellSizes.cellHeightPx)
         .attr("fill", (d) => {return valueToColor(colorScale(d))})

    group.append("text")
         .attr("x", (d,i) => {return cellSizes.cellWidthPx * (i + 0.5) + document.world.sizes.marginLeft + 1})
         .attr("y", (d,i) => {return cellSizes.cellHeightPx * (otherIdx + 0.5) + document.world.sizes.marginTop})
         .attr("width", cellSizes.cellWidthPx)
         .attr("height", cellSizes.cellHeightPx)
         .attr("text-anchor", "middle")
         .attr("alignment-baseline", "central")
         .attr("font-size", "80%")
         .attr("font-family", "Arial, Helvetica, sans-serif")
         .text((d) => {return Math.round(d * 1000) / 1000})
  })
}

const drawAxis = (headers, cellSizes) => {
  const xHeaders = headers.concat([""])
  const yHeaders = [""].concat(headers)
  yHeaders.reverse()
  const xScale = d3.scalePoint()
                   .domain(xHeaders)
                   .range([cellSizes.xAxisMargin , cellSizes.xAxisLength])
  const yScale = d3.scalePoint()
                   .domain(yHeaders)
                   .range([cellSizes.yAxisMargin , cellSizes.yAxisLength])
  const xAxis = d3.axisBottom(xScale)
  const yAxis = d3.axisLeft(yScale)

  document.world
          .heatMap
          .append("g")
          .attr("class", "x_axis")
          .attr("transform", "translate(" + document.world.sizes.marginLeft + "," + (document.world.sizes.marginTop + document.world.sizes.chartHeight) + ")")
          .call(xAxis)
          .selectAll("text")
          .attr("x", -cellSizes.cellWidthPx / 2 + "px")
          .attr("y", cellSizes.cellHeightPx / 2 + "px")
          .attr("transform", "rotate(-70)")
          .attr("font-family", "Arial, Helvetica, sans-serif")

  document.world
          .heatMap
          .append("g")
          .attr("class", "y_axis")
          .attr("transform", "translate(" + document.world.sizes.marginLeft + "," + (document.world.sizes.marginTop - cellSizes.cellHeightPx) + ")")
          .call(yAxis)
          .selectAll("text")
          .attr("y", cellSizes.cellHeightPx / 2 + "px")
          .attr("transform", "rotate(-20)")
          .attr("font-family", "Arial, Helvetica, sans-serif")
}

const mouseOverHandler = (rect, variable1Idx, variable2Idx) => {
  d3.select("#r_" + variable1Idx + "_" + variable2Idx)
    .attr("opacity", 0.5)
}

const mouseOutHandler = (rect, variable1Idx, variable2Idx) => {
  d3.select("#r_" + variable1Idx + "_" + variable2Idx)
    .attr("opacity", 1)
}

const clickHandler = (variable1Idx, variable2Idx) => {
  fillScatter(variable1Idx, variable2Idx)
}
