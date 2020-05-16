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
        data: ['步行', '公共交通', '自驾', '自行车']
    },
    series: [
        {
            name: '出行方式',
            type: 'pie',
            radius: '55%',
            center: ['50%', '60%'],
            data: [
                {value: 131, name: '步行'},
                {value: 39, name: '公共交通'},
                {value: 10, name: '自驾'},
                {value: 57, name: '自行车'}
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