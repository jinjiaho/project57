/**
 * "Class" that models an Chart instance in HTML
 *
 * This "class" packages a few modules together to make displaying charts in HTML easy:
 * 
 *  - Creation/modification of HTML container for displaying charts using Highcharts.js
 *  - Support for multiple charts per page and enlarged modal for finer details
 *  - Display charts with custom sampling types, regression lines, log axes or percentiles
 * 
 * See official documentation for details on using this "class", or look at exisiting implementations.
 * 
 * @param {string} target - CSS selector identifying DOM element to which the chart is anchored to 
 * @param {Object} dataSources - JSON object detailing data to show on chart AND options to customise display of chart
 */

function Chart(target, dataSources) {


    /*===============================
    |          Constructor          |
    ===============================*/

    // Public reference to instance variables
    this.dataSources = dataSources;
    this.target = target; //CSS id of chart container

    // Private instances of the chart
    var masterChart;


    /*==================================
    |          Public Methods          |
    ==================================*/


    /**
        Function that fires the first request to create the chart. Upon
        successful response creates both the detailed and the master chart
    */
    this.createChart = function() {
        // initChartComponents();
        $.ajax({
            type: "POST",
            url: "/api/getData/",
            data: JSON.stringify(dataSources),
            dataType: "json",
            contentType: "application/json",
            processData: false
        }).success(function(data) {

            print(data)



            // Finished updating masterChart. Updating detailchart
            // masterChart.redraw();
            // loadDetailChartData();
        });
    };

    // Call to createChart
    this.createChart();
}