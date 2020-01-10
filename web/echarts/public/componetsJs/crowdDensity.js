var myChart = echarts.init(document.getElementById('crowdDensity'));
// var data = [].push(dataJson["2018-10-03 00:00:00"]);
var hData = heatmapdata;
// console.log(hData);
var convertData = function (data) {
    var points = [].concat.apply([], data.map(function (track) {
                return track.map(function (seg) {
                    return seg.coord.concat([1]);
                });
            }));
    return points;
};

var option = {
baseOption: {
    timeline: {
        show:false,
        autoPlay:true,
        data: ["0:00","1:00","2:00","3:00","4:00","5:00","6:00","7:00","8:00","9:00","10:00","11:00","12:00","13:00","14:00","15:00","16:00","17:00","18:00","19:00","20:00","21:00","22:00","23:00"],
        axisType: 'category',
        padding: [5,5,5,5],
        playInterval:1500,
        lineStyle:{color:'white'},
        label:{
            normal:{
                textStyle:{
                    color: 'white',
                    fontSize: 13
                }
            }
        }
    },
    bmap: {
            center: [123.403043,41.799823],
            zoom: 13,
            roam: true,
            mapStyle: {
             styleJson:[
                {
                    "featureType": "land",
                    "elementType": "geometry",
                    "stylers": {
                        "visibility": "on",
                        "color": "#091220ff"
                    }
                }, {
                    "featureType": "water",
                    "elementType": "geometry",
                    "stylers": {
                        "visibility": "on",
                        "color": "#113549ff"
                    }
                }, {
                    "featureType": "green",
                    "elementType": "geometry",
                    "stylers": {
                        "visibility": "on",
                        "color": "#0e1b30ff"
                    }
                }, {
                    "featureType": "building",
                    "elementType": "geometry",
                    "stylers": {
                        "visibility": "on"
                    }
                }, {
                    "featureType": "building",
                    "elementType": "geometry.fill",
                    "stylers": {
                        "color": "#ffffffb3"
                    }
                }, {
                    "featureType": "building",
                    "elementType": "geometry.stroke",
                    "stylers": {
                        "color": "#dadadab3"
                    }
                }, {
                    "featureType": "subwaystation",
                    "elementType": "geometry",
                    "stylers": {
                        "visibility": "on",
                        "color": "#b15454B2"
                    }
                }, {
                    "featureType": "education",
                    "elementType": "geometry",
                    "stylers": {
                        "visibility": "on",
                        "color": "#e4f1f1ff"
                    }
                }, {
                    "featureType": "medical",
                    "elementType": "geometry",
                    "stylers": {
                        "visibility": "on",
                        "color": "#f0dedeff"
                    }
                }, {
                    "featureType": "scenicspots",
                    "elementType": "geometry",
                    "stylers": {
                        "visibility": "on",
                        "color": "#e2efe5ff"
                    }
                }, {
                    "featureType": "highway",
                    "elementType": "geometry",
                    "stylers": {
                        "visibility": "on",
                        "weight": 4
                    }
                }, {
                    "featureType": "highway",
                    "elementType": "geometry.fill",
                    "stylers": {
                        "color": "#f7c54dff"
                    }
                }, {
                    "featureType": "highway",
                    "elementType": "geometry.stroke",
                    "stylers": {
                        "color": "#fed669ff"
                    }
                }, {
                    "featureType": "highway",
                    "elementType": "labels",
                    "stylers": {
                        "visibility": "on"
                    }
                }, {
                    "featureType": "highway",
                    "elementType": "labels.text.fill",
                    "stylers": {
                        "color": "#8f5a33ff"
                    }
                }, {
                    "featureType": "highway",
                    "elementType": "labels.text.stroke",
                    "stylers": {
                        "color": "#ffffffff"
                    }
                }, {
                    "featureType": "highway",
                    "elementType": "labels.icon",
                    "stylers": {
                        "visibility": "on"
                    }
                }, {
                    "featureType": "arterial",
                    "elementType": "geometry",
                    "stylers": {
                        "visibility": "on",
                        "weight": 2
                    }
                }, {
                    "featureType": "arterial",
                    "elementType": "geometry.fill",
                    "stylers": {
                        "color": "#d8d8d8ff"
                    }
                }, {
                    "featureType": "arterial",
                    "elementType": "geometry.stroke",
                    "stylers": {
                        "color": "#ffeebbff"
                    }
                }, {
                    "featureType": "arterial",
                    "elementType": "labels",
                    "stylers": {
                        "visibility": "on"
                    }
                }, {
                    "featureType": "arterial",
                    "elementType": "labels.text.fill",
                    "stylers": {
                        "color": "#525355ff"
                    }
                }, {
                    "featureType": "arterial",
                    "elementType": "labels.text.stroke",
                    "stylers": {
                        "color": "#ffffffff"
                    }
                }, {
                    "featureType": "local",
                    "elementType": "geometry",
                    "stylers": {
                        "visibility": "on",
                        "weight": 1
                    }
                }, {
                    "featureType": "local",
                    "elementType": "geometry.fill",
                    "stylers": {
                        "color": "#d8d8d8ff"
                    }
                }, {
                    "featureType": "local",
                    "elementType": "geometry.stroke",
                    "stylers": {
                        "color": "#ffffffff"
                    }
                }, {
                    "featureType": "local",
                    "elementType": "labels",
                    "stylers": {
                        "visibility": "on"
                    }
                }, {
                    "featureType": "local",
                    "elementType": "labels.text.fill",
                    "stylers": {
                        "color": "#979c9aff"
                    }
                }, {
                    "featureType": "local",
                    "elementType": "labels.text.stroke",
                    "stylers": {
                        "color": "#ffffffff"
                    }
                }, {
                    "featureType": "railway",
                    "elementType": "geometry",
                    "stylers": {
                        "visibility": "on",
                        "weight": 1
                    }
                }, {
                    "featureType": "railway",
                    "elementType": "geometry.fill",
                    "stylers": {
                        "color": "#123c52ff"
                    }
                }, {
                    "featureType": "railway",
                    "elementType": "geometry.stroke",
                    "stylers": {
                        "color": "#12223dff"
                    }
                }, {
                    "featureType": "subway",
                    "elementType": "geometry",
                    "stylers": {
                        "visibility": "on",
                        "weight": 1
                    }
                }, {
                    "featureType": "subway",
                    "elementType": "geometry.fill",
                    "stylers": {
                        "color": "#d8d8d8ff"
                    }
                }, {
                    "featureType": "subway",
                    "elementType": "geometry.stroke",
                    "stylers": {
                        "color": "#ffffff00"
                    }
                }, {
                    "featureType": "subway",
                    "elementType": "labels",
                    "stylers": {
                        "visibility": "on"
                    }
                }, {
                    "featureType": "subway",
                    "elementType": "labels.text.fill",
                    "stylers": {
                        "color": "#979c9aff"
                    }
                }, {
                    "featureType": "subway",
                    "elementType": "labels.text.stroke",
                    "stylers": {
                        "color": "#ffffffff"
                    }
                }, {
                    "featureType": "continent",
                    "elementType": "labels",
                    "stylers": {
                        "visibility": "on"
                    }
                }, {
                    "featureType": "continent",
                    "elementType": "labels.icon",
                    "stylers": {
                        "visibility": "on"
                    }
                }, {
                    "featureType": "continent",
                    "elementType": "labels.text.fill",
                    "stylers": {
                        "color": "#333333ff"
                    }
                }, {
                    "featureType": "continent",
                    "elementType": "labels.text.stroke",
                    "stylers": {
                        "color": "#ffffffff"
                    }
                }, {
                    "featureType": "city",
                    "elementType": "labels.icon",
                    "stylers": {
                        "visibility": "on"
                    }
                }, {
                    "featureType": "city",
                    "elementType": "labels",
                    "stylers": {
                        "visibility": "on"
                    }
                }, {
                    "featureType": "city",
                    "elementType": "labels.text.fill",
                    "stylers": {
                        "color": "#454d50ff"
                    }
                }, {
                    "featureType": "city",
                    "elementType": "labels.text.stroke",
                    "stylers": {
                        "color": "#ffffffff"
                    }
                }, {
                    "featureType": "town",
                    "elementType": "labels.icon",
                    "stylers": {
                        "visibility": "on"
                    }
                }, {
                    "featureType": "town",
                    "elementType": "labels",
                    "stylers": {
                        "visibility": "on"
                    }
                }, {
                    "featureType": "town",
                    "elementType": "labels.text.fill",
                    "stylers": {
                        "color": "#454d50ff"
                    }
                }, {
                    "featureType": "town",
                    "elementType": "labels.text.stroke",
                    "stylers": {
                        "color": "#ffffffff"
                    }
                }, {
                    "featureType": "road",
                    "elementType": "geometry.fill",
                    "stylers": {
                        "color": "#12223dff"
                    }
                }, {
                    "featureType": "poilabel",
                    "elementType": "labels",
                    "stylers": {
                        "visibility": "on"
                    }
                }, {
                    "featureType": "districtlabel",
                    "elementType": "labels",
                    "stylers": {
                        "visibility": "off"
                    }
                }, {
                    "featureType": "road",
                    "elementType": "geometry",
                    "stylers": {
                        "visibility": "on"
                    }
                }, {
                    "featureType": "road",
                    "elementType": "labels",
                    "stylers": {
                        "visibility": "off"
                    }
                }, {
                    "featureType": "road",
                    "elementType": "geometry.stroke",
                    "stylers": {
                        "color": "#ffffff00"
                    }
                }, {
                    "featureType": "district",
                    "elementType": "labels",
                    "stylers": {
                        "visibility": "off"
                    }
                }, {
                    "featureType": "poilabel",
                    "elementType": "labels.icon",
                    "stylers": {
                        "visibility": "off"
                    }
                }, {
                    "featureType": "poilabel",
                    "elementType": "labels.text.fill",
                    "stylers": {
                        "color": "#2dc4bbff"
                    }
                }, {
                    "featureType": "poilabel",
                    "elementType": "labels.text.stroke",
                    "stylers": {
                        "color": "#ffffff00"
                    }
                }, {
                    "featureType": "manmade",
                    "elementType": "geometry",
                    "stylers": {
                        "color": "#12223dff"
                    }
                }, {
                    "featureType": "districtlabel",
                    "elementType": "labels.text.stroke",
                    "stylers": {
                        "color": "#ffffffff"
                    }
                }, {
                    "featureType": "entertainment",
                    "elementType": "geometry",
                    "stylers": {
                        "color": "#ffffffff"
                    }
                }, {
                    "featureType": "shopping",
                    "elementType": "geometry",
                    "stylers": {
                        "color": "#12223dff"
                    }
                }
            ]
            }
    },
    visualMap: {
            show: false,
            top: 'top',
            min: 0,
            max: 2,
            seriesIndex: 0,
            calculable: true,
            inRange: {
                 color: ['red', 'blue', 'green', 'yellow', 'red']
            },
    },
    series: [{
        type: 'heatmap',
            coordinateSystem: 'bmap',
            pointSize: 10,
            blurSize: 6
    }]
},
options: [
    {
        series:[{
            data : convertData(hData[0])
        }]
    },
    {
        series:[{
            data : convertData(hData[1])
        }]
    },
    {
        series:[{
            data : convertData(hData[2])
        }]
    },
    {
        series:[{
            data : convertData(hData[3])
        }]
    },
    {
        series:[{
            data : convertData(hData[4])
        }]
    },
    {
        series:[{
            data : convertData(hData[5])
        }]
    },
    {
        series:[{
            data : convertData(hData[6])
        }]
    },
    {
        series:[{
            data : convertData(hData[7])
        }]
    },
    {
        series:[{
            data : convertData(hData[8])
        }]
    },
    {
        series:[{
            data : convertData(hData[9])
        }]
    },
    {
        series:[{
            data: convertData(hData[10])
        }]
    },
    {
        series:[{
            data : convertData(hData[11])
        }]
    },
    {
        series:[{
            data : convertData(hData[12])
        }]
    },
    {
        series:[{
            data : convertData(hData[13])
        }]
    },
    {
        series:[{
            data : convertData(hData[14])
        }]
    },
    {
        series:[{
            data : convertData(hData[15])
        }]
    },
    {
        series:[{
            data : convertData(hData[16])
        }]
    },
    {
        series:[{
            data : convertData(hData[17])
        }]
    },
    {
        series:[{
            data : convertData(hData[18])
        }]
    },
    {
        series:[{
            data : convertData(hData[19])
        }]
    },
    {
        series:[{
            data : convertData(hData[20])
        }]
    },
    {
        series:[{
            data: convertData(hData[21])
        }]
    },
    {
        series:[{
            data : convertData(hData[22])
        }]
    },
    {
        series:[{
            data: convertData(hData[23])
        }]
    }
]
}
myChart.setOption(option);
