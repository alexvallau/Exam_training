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
    //- fonction qui prend en paramètre l’état souhaité du robinet et retourne un booléen : on ou off
    
    var clientmqtt  = mqtt.connect('mqtt://localhost:1883');
    clientmqtt.on('connect', function () {
        //console.log("Connected");
        clientmqtt.subscribe('jardin');
    });

    clientmqtt.on('message', function (topic, message) {
        // parsez les données du message et faites ce que vous voulez avec
        console.log("Received message", message.toString());
        //split message with ;
        var message = message.toString().split(";");
        humidite=message[0];
        temperature=message[1];
        text = message.toString();
        io.emit('changetext', text);
    });

    socket.on('buttonClick', function(button){
        console.log('Button clicked:', button);
    
        var client = xmlrpc.createClient({ host: 'localhost', port: 8081 });
    
        // Faites quelque chose en fonction du bouton cliqué
        if (button === 'ouverture') {
            console.log('ouverture');
            client.methodCall('arroser', ['ouverture'], function (error, value) {
                console.log('Result:', value);
            });
        } else if (button === 'fermeture') {
            console.log('fermeture');
            client.methodCall('arroser', ['fermeture'], function (error, value) {
                console.log('Result:', value);
            });
        } else if (button === 'auto') {
            console.log('auto');
            client.methodCall('robinet', ['auto'], function (error, value) {
                console.log('Result:', value);
            });
        }
    });
  

});


