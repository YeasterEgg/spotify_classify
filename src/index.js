const d3 = require('d3')
const HeatMap = require('./lib/heat_map.js').HeatMap
const ScatterPlot = require('./lib/scatter_plot.js').ScatterPlot
const RadialPlot = require('./lib/radial_plot.js').RadialPlot

const w = () => {
  return Math.max(document.documentElement.clientWidth, window.innerWidth || 0)
}
const h = () => {
  return Math.max(document.documentElement.clientHeight, window.innerHeight || 0)
}

const sizes = (w, h) => {
  const sizes = {}
  sizes["w"]            = w
  sizes["h"]            = h
  sizes["marginLeft"]   = w / 15
  sizes["marginRight"]  = w / 30
  sizes["marginTop"]    = h / 30
  sizes["marginBottom"] = h / 10
  sizes["chartWidth"]   = w / 2 - sizes.marginLeft - sizes.marginRight
  sizes["chartHeight"]  = h - sizes.marginTop - sizes.marginBottom
  return sizes
}

const drawCharts = () => {
  fetch("/songs?limit=1000").then( (response) => {
    return response.json()
  }).then( (data) => {
    drawContainer(data)
  })
}

const drawContainer = (data) => {
  const currentSizes = sizes(w(), h())
  const container = d3.select(".charts-container")
                               .append("svg")
                               .attr("width", currentSizes.w)
                               .attr("height", currentSizes.h)
  const heatMap = new HeatMap(currentSizes, container, data)
  const scatterPlot = new ScatterPlot(currentSizes, container, data)
  const radialPlot = new RadialPlot(currentSizes, container, data)
  heatMap.draw(scatterPlot)
  scatterPlot.draw(heatMap, radialPlot)
  radialPlot.draw(heatMap)
}

document.addEventListener('DOMContentLoaded', drawCharts);
