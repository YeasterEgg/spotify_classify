const d3 = require('d3')
const drawHeatMap = require('./lib/heat_map.js').drawHeatMap
const drawScatter = require('./lib/scatter_plot.js').drawScatter
const drawRadial = require('./lib/radial_plot.js').drawRadial

const w = () => {
  return Math.max(document.documentElement.clientWidth, window.innerWidth || 0)
}
const h = () => {
  return Math.max(document.documentElement.clientHeight, window.innerHeight || 0)
}

const sizes = (w, h) => {
  const sizes = {}
  sizes["marginLeft"]   = w / 15
  sizes["marginRight"]  = w / 30
  sizes["marginTop"]    = h / 30
  sizes["marginBottom"] = h / 10
  sizes["chartWidth"]   = w / 2 - sizes.marginLeft - sizes.marginRight
  sizes["chartHeight"]  = h - sizes.marginTop - sizes.marginBottom
  return sizes
}

document.world = {
  w: null,
  h: null,
  container: null,
  heatMap: null,
  scatterPlot: null,
  radialPlot: null,
  data: null,
  visible: "heatMap",
  sizes: null,
}

const drawCharts = () => {
  fetch("/songs?limit=1000").then( (response) => {
    return response.json()
  }).then( (data) => {
    drawContainer(data)
  })
}

const drawContainer = (data) => {
  document.world.w    = w()
  document.world.h    = h()
  document.world.sizes = sizes(document.world.w, document.world.h)
  document.world.data = data
  document.world.container = d3.select(".charts-container")
                               .append("svg")
                               .attr("width", document.world.w)
                               .attr("height", document.world.h)
  drawHeatMap()
  drawScatter()
  drawRadial()
  // window.onResize = () => {redrawAll(container, heatMap)}
}

const redrawAll = (container, heatMap) => {
  container.attr("width", w() )
           .attr("height", h() )
}

document.addEventListener('DOMContentLoaded', drawCharts);
