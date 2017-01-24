import * as d3 from "d3"
import * as heat_map from './lib/heat_map.js'

const chartWidth = window.innerWidth * 0.9
const chartHeight = 640
const margin = {top: chartWidth * 0.1, right: chartHeight * 0.1, bottom: chartWidth * 0.1, left: chartHeight * 0.1};
const width  = chartWidth - margin.left - margin.right
const height = chartHeight - margin.top - margin.bottom

const retrieveData = (url, chartSelector, buttonSelector) => {
  let limit = d3.select("#limit").property("value")
  let limitedUrl = (limit == 0) ? url : url + "?limit=" + limit
  d3.json(limitedUrl, (error, data) => {
    if(data){
      document.variables = data
      const chart = drawChart(chartSelector, "chartSvg")
      console.log(chart)
      createButton(buttonSelector, chartSelector, chart)
    }else{
      reject(Error(error))
    }
  })
}

const createButton = (buttonSelector, chartSelector, chart) => {
  d3.select(buttonSelector + "_button")
    .append("button")
    .text("Draw heatmap")
    .on("click", heat_map.drawChart.bind(this, chartSelector, margin, width, height, chart))
}

const drawChart = (selector, chartClass) => {
  return d3.select(selector)
           .append("svg")
           .classed(chartClass, true)
           .attr("width", width + margin.left + margin.right)
           .attr("height", height + margin.top + margin.bottom)
           .append("g")
           .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
}

const limitButton = () => {
  d3.select("#load").on("click", retrieveData.bind(this, "/songs", ".chart", ".heatmap"))
}

document.addEventListener('DOMContentLoaded', limitButton);
