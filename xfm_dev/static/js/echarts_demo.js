var server_info;
    var colors = ['#0780cf', '#765005', '#fa6d1d', '#0e2c82', '#b6b51f', '#da1f18',
        '#701866', '#f47a75', '#009db2', '#024b51', '#0780cf', '#765005'];
    var colors2 = ['#63b2ee', '#76da91', '#f8cb7f', '#f89588', '#7cd6cf', '#9192ab', '#7898e1',
        '#efa666', '#eddd86', '#9987ce', '#63b2ee', '#76da91'];
    var colors3 = ['#95a2ff', '#fa8080', '#ffc076', '#fae768', '#87e885', '#3cb9fc', '#73abf5',
        '#cb9bff', '#434348', '#90ed7d', '#f7a35c', '#8085e9'];
    var myChart = echarts.init(document.getElementById('main'));
    var option;
    option = {
        title: [
            {
                text: '价格分布',
                textstyle: {fontfamily: 'sans-serif'}
            }
        ],
        backgroundColor: '',
        dataZoom: [
            {
                type: 'slider',
                xAxisIndex: 0,
                start: 0,
                end: 100
            },
            {
                type: 'inside',
                xAxisIndex: 0,
                start: 0,
                end: 100
            },
        ],
        tooltip: [{}],
        legend: [
            {
                data: '{{id}}',
            }
        ],
        toolbox: [{show: true, feature: {saveAsImage: {}}}],
        xAxis: [
            {
                data: [
                    {% for date in dates %}
                        "{{date}}",
                    {% endfor %}],
                splitLine: {show: false}
            }
        ],
        yAxis: [{scale: true, splitLine: {show: false}}],
        series: [
            {
                name: '{{id}}',
                type: 'line',
                markPoint: {
                    data: [
                        {type: 'max', name: '最大值'},
                        {type: 'min', name: '最小值'}]
                },
                data: [
                    {% for price in prices %}
                        "{{price}}",
                    {% endfor %}],
                itemStyle: {
                    normal: {
                        color: colors[0]
                    }
                },
            }

        ]
    };
    myChart.setOption(option, true);