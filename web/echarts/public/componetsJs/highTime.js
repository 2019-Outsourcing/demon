var myChart = echarts.init(document.getElementById('highTime')); 
var option = {
    title: {
        text: '高峰时段',
        left: 'center',
        textStyle:{
            color: '#0099FF',
        }
    },
    xAxis:{
        type:'category',
        data:['0:00','1:00','2:00','3:00','4:00','5:00','6:00','7:00','8:00','9:00','10:00','11:00','12:00','13:00','14:00','15:00','16:00','17:00','18:00','19:00','20:00','21:00','22:00','23:00']
    },
    yAxis:{
        type:'value'
    },
    series: [{
        data: [186,142,81,79,82,89,137,183,201,174,159,151,182,198,252,242,238,218,207,200,250,228],
        type: 'line'
    }]
}

myChart.setOption(option);