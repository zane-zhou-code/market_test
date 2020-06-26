setTimeout(function () {
        $.ajax({
            url: '{% url 'select_query' %}',
            async: true,
            type: 'GET',
            success: function (ret) {
                server_info_f = eval(ret);
                $("option").remove(".selected_item");
                for (var key in server_info_f) {
                    if (key == '618100') {
                        zoption = "<option value=\"" + key + "\" selected>" + server_info_f[key] + "</option>";
                        $("select[name=DIMENSION_select]").append(zoption);
                        $("select[name=DIMENSION_select2]").append(zoption);
                        $("select[name=DIMENSION_select3]").append(zoption);
                    } else if (key == '618000') {
                        zoption = "<option value=\"" + key + "\" selected>" + server_info_f[key] + "</option>";
                        $("select[name=DIMENSION_select2]").append(zoption);
                        $("select[name=DIMENSION_select3]").append(zoption);
                    } else {
                        zoption = "<option value=\"" + key + "\">" + server_info_f[key] + "</option>";
                        $("select[name=DIMENSION_select]").append(zoption);
                        $("select[name=DIMENSION_select2]").append(zoption);
                        $("select[name=DIMENSION_select3]").append(zoption);
                    }
                }

            },
        });
    }, 1000);
    $(function (view1) {
        $("#AJAX_get").click(function () {
            myChart.showLoading();
            var form_data = [];
            form_data = {
                "DIMENSION_select": $("#DIMENSION_select").val(),
                "START_time": $("#START_time").val(),
                "END_time": $("#END_time").val(),
            };
            $.ajax({
                url: '{% url 'market_dates' %}',
                async: true,
                type: 'GET',
                data: form_data,
                success: function (ret) {
                    var series = [];
                    var mid;
                    var mid_id;
                    server_info = eval(ret);
                    option.xAxis[0].data = server_info['DATES'];
                    mid = server_info['ZID'];
                    option.legend[0].data = server_info['ZID_FUC'];
                    console.log(server_info['ZID_FUC']);
                    console.log(server_info['PRICES']);
                    for (var i = 0; i < server_info['ZID'].length; i++) {
                        mid_id = mid[i];
                        console.log(mid_id);
                        console.log(server_info['PRICES'][mid_id]);
                        series.push({
                            name: server_info['ZID_FUC'][i],
                            type: 'line',
                            data: server_info['PRICES'][mid_id],

                            markPoint: {
                                data: [
                                    {type: 'max', name: '最大值'},
                                    {type: 'min', name: '最小值'}],
                            },
                            itemStyle: {
                                normal: {
                                    color: colors[i]
                                }
                            }
                        })
                    }
                    option.series = series;
                    myChart.hideLoading();
                    myChart.setOption(option, true)
                },
                error: function () {            //失败
                    console.log('失败')
                }
            });

        });
        window.onresize = function () {
            myChart.resize();
        };
    });
    $(function (view2) {
        $("#AJAX_get2").click(function () {
            myChart2.showLoading();
            var form_data = {
                "DIMENSION_select2": $("#DIMENSION_select2").val(),
                "START_time2": $("#START_time2").val(),
                "END_time2": $("#END_time2").val(),
            };
            $.ajax({
                url: '{% url 'market_dates2' %}',
                async: true,
                type: 'GET',
                data: form_data,
                success: function (ret) {
                    var data_first;
                    var series = [];
                    server_info = eval(ret);
                    data_first = server_info['RESULT'][0][1];
                    option2.dataset['source'] = server_info['RESULT'];
                    for (var i = 0; i < server_info['RESULT'].length - 1; i++) {
                        series.push({
                            type: 'line',
                            smooth: true,
                            seriesLayoutBy: 'row',
                            symbolSize: 10,
                            itemStyle: {
                                normal: {
                                    color: colors[i]
                                }
                            }
                        })
                    }
                    series.push({
                        type: 'pie',
                        id: 'pie',
                        radius: '30%',
                        center: ['50%', '25%'],
                        label: {
                            formatter: '{d}%'
                        },
                        encode: {
                            itemName: 'DIM_ID',
                            value: data_first,
                            tooltip: data_first
                        },
                        color: colors
                    });
                    option2.series = series;
                    myChart2.hideLoading();
                    myChart2.setOption(option2, true)

                },
                error: function () {            //失败
                    console.log('失败')
                }
            });

        });
        window.onresize = function () {
            myChart2.resize();
        };
    });
    $(function (view3) {
        $("#AJAX_get3").click(function () {
            myChart3.showLoading();
            var form_data = {
                "DIMENSION_select3": $("#DIMENSION_select3").val(),
                "START_time3": $("#START_time3").val(),
                "END_time3": $("#END_time3").val(),
            };
            $.ajax({
                url: '{% url 'market_dates3' %}',
                async: true,
                type: 'GET',
                data: form_data,
                success: function (ret) {
                    var data_first;
                    var series = [];
                    server_info = eval(ret);
                    data_first = server_info['RESULT'][0][1];
                    option3.dataset['source'] = server_info['RESULT'];
                    for (var i = 0; i < server_info['RESULT'].length - 1; i++) {
                        series.push({
                            type: 'line',
                            smooth: true,
                            seriesLayoutBy: 'row',
                            symbolSize: 10,
                            itemStyle: {
                                normal: {
                                    color: colors[i]
                                }
                            }
                        })
                    }
                    series.push({
                        type: 'bar',
                        id: 'pie',
                        xAxisIndex: 1,
                        yAxisIndex: 1,
                        label: {
                            formatter: '{d}%'
                        },
                        encode: {
                            x: 'DIM_ID',
                            y: data_first
                        },
                        itemStyle: {
                            normal: {
                                //这里是重点
                                color: function (params) {
                                    //注意，如果颜色太少的话，后面颜色不会自动循环，最好多定义几个颜色

                                    return colors[params.dataIndex]
                                }
                            }
                        },
                    });
                    option3.series = series;
                    myChart3.hideLoading();
                    myChart3.setOption(option3, true)

                },
                error: function () {            //失败
                    console.log('失败')
                }
            });

        });
        window.onresize = function () {
            myChart3.resize();
        };
    });
    setTimeout(function (view2) {
        myChart2.on('mouseover', function (params) {
            if (params.componentType == "xAxis") {
                var xAxisInfo = params.value;
                myChart2.setOption({
                    series: {
                        id: 'pie',
                        label: {
                            formatter: '{d}%'
                        }, encode: {
                            value: xAxisInfo,
                            tooltip: xAxisInfo
                        }
                    }
                });
            }
            if (params.componentType == "series" && params.seriesType == 'line') {
                var xAxisInfo = params.value[0];
                myChart2.setOption({
                    series: {
                        id: 'pie',
                        label: {
                            formatter: '{d}%'
                        },
                        encode: {
                            value: xAxisInfo,
                            tooltip: xAxisInfo
                        }
                    }

                });
            }
            setTimeout(function () {
                myChart.dispatchAction({
                    type: 'highlight',
                    seriesIndex: 4,
                    dataIndex: params.seriesIndex
                });
            }, 300);
        });

        myChart2.on('mouseout', function (params) {
            myChart2.dispatchAction({
                type: 'downplay',
                seriesIndex: 4,
                dataIndex: params.seriesIndex
            });
        });
    }, 100);
    setTimeout(function (view3) {
        myChart3.on('mouseover', function (params) {
            if (params.componentType == "xAxis") {
                var xAxisInfo = params.value;
                myChart3.setOption({
                    series: {
                        id: 'pie',
                        label: {
                            formatter: '{d}%'
                        }, encode: {
                            y: xAxisInfo
                        },
                        itemStyle: {
                            normal: {
                                //这里是重点
                                color: function (params) {
                                    //注意，如果颜色太少的话，后面颜色不会自动循环，最好多定义几个颜色

                                    return colors[params.dataIndex]
                                }
                            }
                        },
                    }
                });
            }
            if (params.componentType == "series" && params.seriesType == 'line') {
                var xAxisInfo = params.value[0];
                myChart3.setOption({
                    series: {
                        id: 'pie',
                        label: {
                            formatter: '{d}%'
                        },
                        encode: {
                            y: xAxisInfo
                        },
                        itemStyle: {
                            normal: {
                                //这里是重点
                                color: function (params) {
                                    //注意，如果颜色太少的话，后面颜色不会自动循环，最好多定义几个颜色

                                    return colors[params.dataIndex]
                                }
                            }
                        },
                    }

                });
            }
            setTimeout(function () {
                myChart3.dispatchAction({
                    type: 'highlight',
                    seriesIndex: 4,
                    dataIndex: params.seriesIndex
                });
            }, 300);
        });

        myChart3.on('mouseout', function (params) {
            myChart3.dispatchAction({
                type: 'downplay',
                seriesIndex: 4,
                dataIndex: params.seriesIndex
            });
        });
    }, 100);