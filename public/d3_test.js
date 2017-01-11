retrieveData = function(url){
  d3.text(url, function(error, data){
    if(error){
      console.log("Something went wrong...")
    }else{
      parsed = JSON.parse(data)
      let songs = parsed.stats
      let arrayed_average = Object.keys(songs).map(function (key) { return songs[key] / parsed.stats["total_songs"] });
      drawChart(arrayed_average, ".chart")
    }
  })
}

drawChart = function(data, selector){
  x = d3.scaleLinear().domain([d3.min(data), d3.max(data)]).range([0, window.innerWidth])
  chart = d3.select(".chart")
  bar = chart.selectAll("div")
  barUpdate = bar.data(data)
  barEnter = barUpdate.enter().append("div")
  barEnter.style("width", function(d) { return x(d) + "px"; }).style("background-color", "lightblue")
  barEnter.text(function(d) { return d; });
}

document.addEventListener('DOMContentLoaded', retrieveData("/songs?limit=10"), false);
