import * as d3 from "d3"
import * as scatter_plot from './scatter_plot.js'

const valueToColor = (value) => {
  if(value >= 0){
    let others = ("00" + (255 - Math.ceil(value)).toString(16)).slice(-2)
    return "#" + others + others + "ff"
  }else{
    let others = ("00" + (255 + Math.ceil(value)).toString(16)).slice(-2)
    return "#ff" + others + others
  }
}

const drawChart = (chartSelector, margin, width, height, chart) => {
  // let chart = d3.select(".chartSvg")
  let plot = chart.append("svg")
                  .attr("id", "plot")

  let matrix = document.variables["cov"]
  let headers = document.variables["headers"]["numeric"]
  let variable_no = matrix.length
  let cell_size = 100 / matrix.length
  let colorScale = d3.scaleLinear().domain([-1, 1]).range([-255, 255])
  let axisWidth = width - width / (2 * variable_no)
  let axisHeight = height - height / (2 * variable_no)

  let xScale = d3.scalePoint()
                 .domain(headers)
                 .range([0, width])

  let yScale = d3.scalePoint()
                 .domain(headers)
                 .range([0, height])

  let xAxis = d3.axisTop(xScale)
  let yAxis = d3.axisLeft(yScale)

  matrix.map((variable, idx) => {
    let group = plot.append("g")
                    .selectAll("rect")
                    .data(variable)
                    .enter()
                    .append("g")
                    .attr("id", (d, i) => {return "r_" + idx + "_" + i})
                    .on("mouseover", (d, i) => {mouseOverHandler(d, idx, i)} )
                    .on("mouseout", (d, i) => {mouseOutHandler(d, idx, i)} )
                    .on("click", (d, i) => {clickHandler(d, idx, i)} )

    group.append("rect")
         .attr("x", (d,i) => {return cell_size * i + "%"})
         .attr("y", (d,i) => {return cell_size * idx + "%"})
         .attr("rx", 5)
         .attr("ry", 5)
         .attr("width", cell_size + "%")
         .attr("height", cell_size + "%")
         .attr("fill", (d) => {return valueToColor(colorScale(d))})

    group.append("text")
         .attr("x", (d,i) => {return cell_size * (i + 0.5)+ "%"})
         .attr("y", (d,i) => {return cell_size * (idx + 0.5) + "%"})
         .attr("width", cell_size + "%")
         .attr("text-anchor", "middle")
         .attr("alignment-baseline", "central")
         .attr("height", cell_size + "%")
         .text((d) => {return Math.round(d * 1000) / 1000})

  })

  chart.append("g")
       .attr("class", "x axis")
       .attr("transform", "translate(0," + height + ")")
       .call(xAxis)

  chart.append("g")
       .attr("class", "y axis")
       .call(yAxis)
}

const mouseOverHandler = (rect, variable1Idx, variable2Idx) => {
  console.log(rect)
  console.log(variable1Idx)
  console.log(variable2Idx)
  d3.select("#r_" + variable1Idx + "_" + variable2Idx)
    .attr("opacity", 0.5)
}

const mouseOutHandler = (rect, variable1Idx, variable2Idx) => {
  console.log(rect)
  console.log(variable1Idx)
  console.log(variable2Idx)
  d3.select("#r_" + variable1Idx + "_" + variable2Idx)
    .attr("opacity", 1)
}

const clickHandler = (rect, variable1Idx, variable2Idx) => {
  console.log(rect)
  console.log(variable1Idx)
  console.log(variable2Idx)
  // d3.select("#plot")
  //   .attr("opacity", 0.5)
}


module.exports = {
  drawChart: drawChart
}
