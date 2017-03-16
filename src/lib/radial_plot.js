const d3 = require('d3')
const baseValue = 30
const multiplier = 270
let headers
let angle
let baseRadiusGenerator
let radiusGenerator

export const drawRadial = () => {
  document.world.radialPlot = document.world
                                      .container
                                      .append("g")
                                      .attr("class", "charts-radialPlot_container")
                                      .style("display", "none")
                                      .style("opacity", 0)
                                      .attr("transform", "translate(" + (document.world.w/4) + "," + (document.world.h/2) + ")")
                                      .on("click", () => {
                                        hideThis()
                                      })

  document.world.radialLine = document.world
                                      .radialPlot
                                      .selectAll("path")

  headers = document.world.data["headers"]["numeric"]
  angle = 2 * Math.PI / (headers.length - 3)

  let emptySong = []
  for(let i = 0; i < headers.length - 3; i++){
    emptySong.push(0)
  }

  baseRadiusGenerator = d3.arc()
                          .innerRadius(0)
                          .outerRadius(baseValue)
                          .startAngle((d, i) => {return i * angle})
                          .endAngle((d, i) => {return (i + 1) * angle})

  radiusGenerator = d3.arc()
                      .innerRadius(0)
                      .outerRadius((d, i) => {return baseValue + d * multiplier})
                      .startAngle((d, i) => {return i * angle})
                      .endAngle((d, i) => {return (i + 1) * angle})

  document.world
          .radialLine
          .data(emptySong)
          .enter()
          .append("path")
          .attr("d", baseRadiusGenerator)
}

export const fillRadial = (song) => {
  const values = song.values
  delete values.count
  delete values.importance
  delete values.popularity
  const color = (song.mood == "sad") ? "red" : "blue"

  if(document.world.visible == "heatMap"){
    showThis( (values) => {
      document.world
              .radialPlot
              .selectAll("path")
              .data(Object.values(values))
              .transition()
              .duration(500)
              .ease(d3.easeQuadInOut)
              .attr("d", radiusGenerator)
    }, values)
  }

  document.world
          .radialPlot
          .selectAll("path")
          .data(Object.values(values))
          .transition()
          .duration(500)
          .ease(d3.easeQuadInOut)
          .attr("d", radiusGenerator)
          .attr("fill", (d) => {return partialColor(d, color)})
}

const showThis = (callback, values) => {
  document.world
          .heatMap
          .transition()
          .duration(500)
          .style("opacity", 0)
          .on("end", () => {
            document.world.heatMap.style("display", "none")
            document.world.radialPlot.style("display", "block")
            document.world.visible = "radialPlot"
            document.world
                    .radialPlot
                    .transition()
                    .duration(500)
                    .style("opacity", 1)
                    .on("end", () => {
                      callback(values)
                    })
          })
}

const hideThis = () => {
  document.world
          .radialPlot
          .transition()
          .duration(500)
          .style("opacity", 0)
          .on("end", () => {
            document.world.radialPlot.style("display", "none")
            document.world.heatMap.style("display", "block")
            document.world
                    .heatMap
                    .transition()
                    .duration(500)
                    .style("opacity", 1)
            document.world.visible = "heatMap"
          })
}

const partialColor = (value, color) => {
  const result = 235 - Math.floor(value * 234)
  const stringedResult = "0" + result.toString(16)
  switch(color){
    case "red":
      return "#" + "ff" + stringedResult.substr(-2,2) + stringedResult.substr(-2,2)
    break
    case "green":
      return "#" + stringedResult.substr(-2,2) + "ff" + stringedResult.substr(-2,2)
    break
    case "blue":
      return "#" + stringedResult.substr(-2,2) + stringedResult.substr(-2,2) + "ff"
    break
  }

}
