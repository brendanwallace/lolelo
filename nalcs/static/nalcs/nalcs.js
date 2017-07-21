
// Toggle between standings/matches.

function toggleStandingsMatches(on, off) {
    document.getElementById(on).classList.remove("display-none");
    document.getElementById(off).classList.add("display-none");
    document.getElementById(on + "-select").classList.add("selected");
    document.getElementById(off + "-select").classList.remove("selected");
}


toggleStandingsMatches("standings", "matches");

// Standings table:

function camelCaseToSpaced(camelCaseString) {
    return camelCaseString.replace(/([A-Z])/g, function(match) {
       return " " + match;
    });
}

// This should be embedded json in the page:
var data = nalcs_standings_data;

var table = d3.select("#nalcs_standings_table");

var sortKey = "rating";
var descending = true;

var ths = d3.select("#nalcs_standings_headings_row").selectAll("th");

    // Assuming the first team has all the data...
ths.data(d3.keys(data[0]))
    .enter()
    .append("th")
    .text(function(d){ return camelCaseToSpaced(d); })
    .attr("class", function(d){ return d; })
    .on("click", function(d) {
        d3.select("#nalcs_standings_headings_row").selectAll('th')
            .classed('ascending', false)
            .classed('descending', false);
        if (sortKey === d) {
            descending = !descending
        } else {
            descending = true;
        }
        sortKey = d;
        if (descending) {
            rows.sort(function(a, b) { return a[d].sort < b[d].sort });
            this.classList.add('descending');
        } else {
            rows.sort(function(a, b) { return a[d].sort > b[d].sort });
            this.classList.add('ascending');
        }
    });

var rows = table.append('tbody').selectAll('tr')
           .data(data)
           .enter()
           .append('tr');

var tds = rows.selectAll('td')
    .data(function(d) { return d3.entries(d); })
    .enter()
    .append('td')
    .attr('class', function(d) { return d.key; });

// Add images to the 'team' column.
tds.filter(function(d) { return d.key === 'team'; })
    .selectAll('img')
    .data(function(d) { return [d]; })
    .enter()
    .insert('img', ':first-child')
    .attr('src', function(d) { return d.value.icon; })
    .attr('class', 'team-icon');

tds.selectAll('span')
    .data(function(d) { return [d]; })
    .enter()
    .append('span')
    .text(function(d) { return d.value.display })
    .append('span')
    .text(function(d) { return d.value.delta })
    .attr('class', function(d) { return d.value.delta_sign })
    .attr('title', "change since 3 days ago");

function toggleWeek(week) {
    var weekDivs = document.getElementsByClassName("week");
    var weekToggles = document.getElementsByClassName("week-toggle");
    for (var i = 0; i < weekDivs.length; i++) {
        weekDivs[i].classList.add("display-none");
        weekToggles[i].classList.remove("selected");
    }
    weekDivs[week - 1].classList.remove("display-none");
    weekToggles[week - 1].classList.add("selected");
}

// This needs to be in the html:
toggleWeek(weekToToggle);