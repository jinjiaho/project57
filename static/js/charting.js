{
    rangeSelector: {
        selected: 1
    },
    tooltip: {
        borderRadius: 6
        // headerFormat: '',
        // pointFormat: '<b>Remaining:</b> {point.y:.0f}'
    },
    credits: {
        enabled: false
    },
    scrollbar: {
        enabled: false
    },
    colors: [
        "#0086B2",
        "#B25A26",
        "#C4F0FF",
        "#FFB364",
        "#64D8FF",
        "#ECD078",
        "#53777A",
        "#D95B43",
        "#542437",
        "#C02942"
    ],
    legend: {
        enabled: true,
        verticalAlign: "top",
        itemStyle: {
            color: '#333',
            fontWeight: 'bold',
            fontSize: '14px'
        }
    },
    xAxis: {
        type: "datetime",
        ordinal: false,
        labels: {
            style: {
                fontSize:'14px'
            }
        }
    },
    yAxis: {
        gridLineDashStyle: 'longdash',
        labels: {
            style: {
                fontSize:'14px'
            }
        }
    },
    chart: {
        type: 'line',
        style: {
            fontFamily: "-apple-system,system-ui,BlinkMacSystemFont,\"Segoe UI\",Roboto,\"Helvetica Neue\",Arial,sans-serif",
            fontSize: "14px"
        }
    },
    plotOptions: {
        area: {
            stacking: "normal",
            connectNulls: false,
            lineColor: "#666666",
            lineWidth: 1,
            marker: {
                lineWidth: 1,
                lineColor: "#666666"
            }
            // fillColor: {
            //     linearGradient: {
            //         x1: 0,
            //         y1: 0,
            //         x2: 0,
            //         y2: 1
            //     },
            //     stops: [
            //         [0, Highcharts.getOptions().colors[0]],
            //         [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
            //     ]
            // },
            // marker: {
            //     enabled: false
            // },
            // lineWidth: 1,
            // states: {
            //     hover: {
            //         lineWidth: 1
            //     }
            // },
            // threshold: null
        },
        series: {
            events: {
              afterAnimate: function(e) {
                // console.log(data)
                // console.log(e)
                // console.log('fired only once for each series');
                // $("#update").css("display", "inline");
                $("#update").fadeIn();
              }
            }
        }
    }
}