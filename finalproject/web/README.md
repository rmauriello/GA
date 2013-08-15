Data Science Data Visualization
--

Visualization of real-time and historical twitter data and associated predictions/classifications:


1) tw_map.html - Based off Mike Bostock's example choropleth (http://bl.ocks.org/mbostock/4060606)
- [X] Add map projections
- [ ] Adjust color map, probably divergent. Or use colorbrewer palettes. 
- [X] Need default color for counties with no tweets 
- [ ] Need way to autorefresh as new data files are created
- [X] Hover text for county FIPS code, name, population, twitter count

2) twitter.tsv - raw tweet count. Should correlate to population. As is typical of count data, follows a "Poisson" distribution. Haven't done statistical testing but it's at least a very close approximation. The log transform also looks like a very good approximation of a normal distribution. Could log transform to help the browser.

3) twitterN.tsv - log of location quotient, scaled to 0-1. Shows exceptions to population trends.

4) [X] tw_dash.html - dashboard containing map, time series, top10, etc.

5) dashboard_sketch.jpg - some ideas on possible dashboard


   
