var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var xmlrpc = require('xmlrpc');
var mqtt = require('mqtt');

app.get('/', function(req, res){
    res.sendFile(__dirname +'/index.html')
});
http.listen(8080, function(){
    console.log('serveur en écoute sur le port 8080');
});




io.on('connection', function(socket){
   
   
    var clientmqtt  = mqtt.connect('mqtt://localhost:1883');
    clientmqtt.on('connect', function () {
        //console.log("Connected");
        clientmqtt.subscribe('jardin');
    });

    clientmqtt.on('message', function (topic, message) {
        // parsez les données du message et faites ce que vous voulez avec
        console.log("Receive message", message.toString());
        //split message with ;
        var message = message.toString().split(";");
        humidite=message[0];
        temperature=message[1];

        text = message.toString();

       io.emit('changetext', text);
    });
  

});


