//WORKING
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

//function to send message to mqtt
function sendMqttMessage(topic, message){
    var client = mqtt.connect('mqtt://localhost');
    client.on('connect', function(){
        client.publish(topic, message);
        client.end();
    });
}

compte_en_banque = 0;


// create mqtt subscriber
var client = mqtt.connect('mqtt://localhost');
client.on('connect', function(){
    console.log('connected to the python publisher');
    client.subscribe('compte_en_banque');
});

client.on('message', function(topic, message){
    console.log('Compte en banque reçu dans serveur: ' + message.toString());
    compte_en_banque = parseInt(message.toString());
    io.emit('setBankAccount', compte_en_banque);
});


io.on('connection', function(socket){
    console.log('a user connected');
    socket.on('buttonClickedAdd', function(amount){
        console.log('button clicked add: ' + amount);
        sendMqttMessage('banque/add', 'add;'+amount);
        
    });

    socket.on('buttonClickedSub', function(amount){
        console.log('button clicked substraction: ' + amount);
        sendMqttMessage('banque/sub', 'sub;'+amount);
    });

    socket.on('buttonClickedCheck', function(){
        console.log('Button clicked check');
        sendMqttMessage('banque/askCheck', 'check;');
    });

});