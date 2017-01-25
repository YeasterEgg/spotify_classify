import * as d3 from "d3"
import * as scatter_plot from './scatter_plot.js'

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

const drawChart = (chart, scatterplot, containerDimensions) => {
  const sizes = document.chartSizes
  const plot = chart.append("g")
                    .append("svg")
                    .attr("id", "heatmap_plot")
                    .attr("width", sizes.width + "px")
                    .attr("height", sizes.height + "px")
                    .attr("x", sizes.marginLeft + "px")
                    .attr("y", sizes.marginTop + "px")

  const matrix = document.variables["cov"]
  const headers = document.variables["headers"]["numeric"]
  const variable_no = matrix.length
  const cellSizePerc = 100 / variable_no
  const cellWidthPx = sizes.width / variable_no
  const cellHeightPx = sizes.height / variable_no
  const colorScale = d3.scaleLinear().domain([-1, 1]).range([-255, 255])
  const xAxisLength = sizes.width - sizes.width / (2 * variable_no)
  const xAxisMargin = sizes.width / (2 * variable_no)
  const yAxisLength = sizes.height - sizes.height / (2 * variable_no)
  const yAxisMargin = sizes.height / (2 * variable_no)

  const xScale = d3.scalePoint()
                   .domain(headers)
                   .range([xAxisMargin , xAxisLength])

  const yScale = d3.scalePoint()
                   .domain(headers)
                   .range([yAxisMargin , yAxisLength])

  const xAxis = d3.axisBottom(xScale)
  const yAxis = d3.axisLeft(yScale)

  matrix.map((variable, idx) => {
    const group = plot.append("g")
                      .selectAll("rect")
                      .data(variable)
                      .enter()
                      .append("g")
                      .attr("id", (d, i) => {return "r_" + idx + "_" + i})
                      .on("mouseover", (d, i) => {mouseOverHandler(d, idx, i)} )
                      .on("mouseout", (d, i) => {mouseOutHandler(d, idx, i)} )
                      .on("click", (d, i) => {clickHandler(d, idx, i, scatterplot)} )

    group.append("rect")
         .attr("x", (d,i) => {return cellSizePerc * i + "%"})
         .attr("y", (d,i) => {return cellSizePerc * idx + "%"})
         .attr("rx", 5)
         .attr("ry", 5)
         .attr("width", cellSizePerc + "%")
         .attr("height", cellSizePerc + "%")
         .attr("fill", (d) => {return valueToColor(colorScale(d))})

    group.append("text")
         .attr("x", (d,i) => {return cellSizePerc * (i + 0.5)+ "%"})
         .attr("y", (d,i) => {return cellSizePerc * (idx + 0.5) + "%"})
         .attr("width", cellSizePerc + "%")
         .attr("text-anchor", "middle")
         .attr("alignment-baseline", "central")
         .attr("height", cellSizePerc + "%")
         .attr("font-size", "80%")
         .attr("font-family", "Arial, Helvetica, sans-serif")
         .text((d) => {return Math.round(d * 1000) / 1000})
  })

  chart.append("g")
       .attr("class", "x axis")
       .attr("transform", "translate(" + sizes.marginLeft + "," + (sizes.marginTop + sizes.height) + ")")
       .call(xAxis)
       .selectAll("text")
       .attr("x", cellWidthPx / 2 + "px")
       .attr("transform", "rotate(45)")
       .attr("font-family", "Arial, Helvetica, sans-serif")

  chart.append("g")
       .attr("class", "y axis")
       .attr("transform", "translate(" + sizes.marginLeft + "," + sizes.marginTop + ")")
       .call(yAxis)
       .selectAll("text")
       .attr("y", "-" + cellHeightPx / 2 + "px")
       .attr("x", "5px")
       .attr("transform", "rotate(-45)")
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

const clickHandler = (rect, variable1Idx, variable2Idx, scatterplot) => {
  console.log(variable1Idx,variable2Idx)
  scatter_plot.drawChart(variable1Idx, variable2Idx, scatterplot)
}


module.exports = {
  drawChart: drawChart
}
