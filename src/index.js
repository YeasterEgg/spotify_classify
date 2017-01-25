import * as d3 from "d3"
import * as heat_map from './lib/heat_map.js'

const drawChartContainer = (chartSelector) => {
  return d3.select(chartSelector)
           .append("svg")
           .attr("width", "100%")
           .attr("height", "100%")
}

const drawHeatmap = () => {
  const limitedUrl = "/songs?limit=1000"
  d3.json(limitedUrl, (error, data) => {
    if(data){
      document.variables = data
      const sizes = d3.select(".chart_box").node().getBoundingClientRect()

      document.chartSizes = {
        width: sizes.width * 0.85,
        height: sizes.height * 0.85,
        marginLeft: sizes.width * 0.10,
        marginRight: sizes.width * 0.05,
        marginTop: sizes.width * 0.05,
        marginBottom: sizes.width * 0.10,
      }

      const heatmap = drawChartContainer(".heatmap")
      const scatterplot = drawChartContainer(".scatterplot")
      heat_map.drawChart(heatmap, scatterplot, sizes)
    }else{
      Error(error)
    }
  })

}

document.addEventListener('DOMContentLoaded', drawHeatmap);
