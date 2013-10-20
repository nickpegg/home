// TODO use proper Javascript namespacing. I'm such a JS nooob!

fetchWeight = function() {
    var chart = this;
    chart.showLoading();

    $.ajax({
        dataType: "json",
        url: fetch_url,
        success: function(data) {
            var points = data[0].data;

            // Update the chart
            chart.series[0].setData(points);
            chart.hideLoading();
            chart.redraw();
        },
    });
};

chartOptions = {
    chart: {
        renderTo: '',
        type: 'spline',
        events: {
            load: fetchWeight
        },
    },
    title: {
        text: '',
    },
    xAxis: {
        type: 'datetime',
        title: {
            text: 'Time'
        },
        dateTimeLabelFormats: { // don't display the dummy year
            month: '%e. %b',
            year: '%b'
        }
    },
    yAxis: {
        title: {
            text: 'Weight (lbs)'
        }
    },
    series: [{
        name: "weight",
        data: [],
    }],
};

