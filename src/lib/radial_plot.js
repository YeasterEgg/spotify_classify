const d3 = require('d3')

export class RadialPlot{
  constructor(sizes, container, data){
    this.sizes       = sizes
    this.container   = container
    this.chart       = null
    this.plot        = null
    this.visible     = false

    this.angle = 2 * Math.PI / (data["headers"]["numeric"].length - 3)
    this.emptySong = (new Array(data["headers"]["numeric"].length - 3)).fill(0)
    this.baseValue = 30
    this.multiplier = 270
  }

  draw(heatMap){
    this.heatMap = heatMap
    this.chart = this.container
                     .append("g")
                     .attr("class", "charts-radialPlot_container")
                     .style("display", "none")
                     .style("opacity", 0)
                     .attr("transform", "translate(" + (this.sizes.w/4) + "," + (this.sizes.h/2) + ")")
                     .on("click", () => {
                       this.hide()
                     })

    this.plot = this.chart.selectAll("path")
    this.baseRadiusGenerator = d3.arc()
                                 .innerRadius(0)
                                 .outerRadius(this.baseValue)
                                 .startAngle((d, i) => {return i * this.angle})
                                 .endAngle((d, i) => {return (i + 1) * this.angle})

    this.radiusGenerator = d3.arc()
                             .innerRadius(0)
                             .outerRadius((d, i) => {return this.baseValue + d * this.multiplier})
                             .startAngle((d, i) => {return i * this.angle})
                             .endAngle((d, i) => {return (i + 1) * this.angle})

    this.plot
        .data(this.emptySong)
        .enter()
        .append("g")
        .append("path")
        .attr("d", this.baseRadiusGenerator)
  }

  fill(song){
    this.show()
    const values = song.values
    delete values.count
    delete values.importance
    delete values.popularity

    this.chart
        .selectAll("path")
        .data(Object.values(values))
        .transition()
        .duration(500)
        .ease(d3.easeQuadInOut)
        .attr("d", this.radiusGenerator)
        .attr("fill", (d) => {console.log(d); return this.partialColor(d, song)})

    this.plot.on("mouseover", (d, i) => {showData(d, i)} )
    this.plot.on("mouseout", (d, i) => {hideData(d, i)}  )
  }

  hide(){
    this.chart
        .transition()
        .duration(500)
        .style("opacity", 0)
        .on("end", () => {
          this.chart.style("display", "none")
          this.heatMap.show()
        })
  }

  show(){
    if(!this.visible){
      this.chart
          .style("display", "block")
          .transition()
          .duration(500)
          .style("opacity", 1)
    }
  }

  partialColor(value, song){
    const result = 235 - Math.floor(value * 234)
    const stringedResult = "0" + result.toString(16)
    switch(song.mood){
      case "sad":
        return "#" + "ff" + stringedResult.substr(-2,2) + stringedResult.substr(-2,2)
      break
      case "happy":
        return "#" + stringedResult.substr(-2,2) + stringedResult.substr(-2,2) + "ff"
      break
    }
  }
}
