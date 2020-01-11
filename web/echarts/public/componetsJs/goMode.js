var myChart = echarts.init(document.getElementById('goMode'));
option = {
    title: {
        text: '出行方式统计',
        left: 'center',
        textStyle:{
            color: '#0099FF',
        }
    },
    tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b} : {c} ({d}%)'
    },
    legend: {
        orient: 'vertical',
        left: 'left',
        textStyle:{
            color: '#0099FF',
        },
        data: ['步行', '地铁', '公交', '私家车', '自行车']
    },
    series: [
        {
            name: '出行方式',
            type: 'pie',
            radius: '55%',
            center: ['50%', '60%'],
            data: [
                {value: 335, name: '步行'},
                {value: 310, name: '地铁'},
                {value: 234, name: '公交'},
                {value: 135, name: '私家车'},
                {value: 1548, name: '自行车'}
            ],
            emphasis: {
                itemStyle: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            }
        }
    ]
};
myChart.setOption(option);