$(document).ready(function() {

	/**
	 * Define chart type and data to extract, as well as relevant config options and metadata
	 */
	var chartData = {
	    rangeSelector: {
	        selected: 1
	    },
	    chart: {
	        type: 'area'
	    },
	    title: {
	        text: 'Item name'
	    },
	    subtitle: {
	        text: 'Quantity remaining'
	    },
	    // xAxis: {
	    //     type: 'datetime',
	    //     dateTimeLabelFormats: { // don't display the dummy year
	    //         month: '%e. %b',
	    //         year: '%b'
	    //     },
	    //     title: {
	    //         text: 'Date'
	    //     }
	    // },
	    tooltip: {
	        // headerFormat: '<b>Quantity</b><br>',
	        pointFormat: '<b>Quantity:</b> {point.y:.2f}'
	    },
	    credits: {
	        enabled: false
	    },
	    scrollbar: {
	        enabled: false
	    },

	    plotOptions: {
	        area: {
	            fillColor: {
	                linearGradient: {
	                    x1: 0,
	                    y1: 0,
	                    x2: 0,
	                    y2: 1
	                },
	                stops: [
	                    [0, Highcharts.getOptions().colors[0]],
	                    [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
	                ]
	            },
	            marker: {
	                enabled: false
	            },
	            lineWidth: 1,
	            states: {
	                hover: {
	                    lineWidth: 1
	                }
	            },
	            threshold: null
	        },
	        series: {
	            events: {
	              afterAnimate: function (ev) {
	                // console.log(data)
	                // console.log(ev)
	                // console.log('fired only once for each series');
	                // $("#update").css("display", "inline");
	                $("#update").fadeIn();
	              }
	            }
	        }
	    },

	    series: [{
	        name: 'Item name'
	        // Define the data points. All series have a dummy year
	        // of 1970/71 in order to be compared on the same x axis. Note
	        // that in JavaScript, months start at 0 for January, 1 for February etc.
		}]}

	/**
	 * Initialise chart on webpage and create nav dropdown for chart (necessary if more thanone chart is present on the page
	 */
	window.chartInstances = [new Chart("chart", chartData)];
	createMenu(window.chartInstances);

});