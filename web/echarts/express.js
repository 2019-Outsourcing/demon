/*
 express.js: 引入 express 模块，设置路由
*/
var expressO = require('express');
var express = require('express')(); //express构建的实例对象

express.get('/', function (request, response) { // 路由
  response.render('shenyang')
})
express.listen(8080) //监听3000端口，默认localhost: 127.0.0.1 || 0.0.0.0
// express.listen(80)
/*
  express.js引入本地静态文件
*/
express.use(expressO.static(__dirname + '/public'));

/*
 express.js: 配置引擎
*/
express.set('views', './views'); // 添加视图路径
express.engine('html', require('ejs').renderFile); // 将EJS模板映射至".html"文件
express.set('view engine', 'html'); // 设置视图引擎

/*
 express.js: 配置引擎
*/
express.get('/shenyang', function (request, response) {
  response.render('shenyang')
})

// express.get('/shenyangjz',function(request,response){
//   response.render('shenyangjz')
// })
// express.get('/shenyangchuxing',function(request,response){
//   response.render('shenyangchuxing')
// })