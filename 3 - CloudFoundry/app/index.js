const express = require("express");

const app = express();

app.use(express.static(__dirname + '/public'));

app.set('view engine', 'pug');

app.get('/', function(req, res){
  
  res.render('main', {
    title: 'Fujitsu Cloud K5 ',
    message: 'Welcome to Fujitsu Cloud K5!!'
  });  
});

app.listen(process.env.PORT || 8080, function () {
  console.log('App listening on port '+ (process.env.PORT !== undefined ? process.env.PORT : 8080) +'');
});