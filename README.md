# Correction exmaen
## Coder le serveur web:
On cherche à coder une application qui permettra à un client, en web, d'ajouter, retirer ou de consulter son compte en banque.
#### Server.js:

```  JS
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
```

#### index.html:
``` html
<!DOCTYPE html>
<html>
<head>
    <title>Number Input</title>
</head>
<body>
    <h1>Compte en banque</h1>
    <div id="compte_en_banque"></div>
    <input type="number" id="numberInput" placeholder="Enter a number">
    <br><br>
    <button id="add" >Ajouter</button>
    <button id="remove">Retirer</button>
    <button id="check">Voir compte</button>
```
## Coder l'intéraction entre la page web html et le javascript(websocket)
#### ServerJS
``` js
io.on('connection', function(socket){
    console.log('a user connected');

    //On code ensuite les différents boutons 
    socket.on('buttonClickedAdd', function(amount){
        console.log('button clicked add: ' + amount);
        sendMqttMessage('banque/add', 'add;'+amount);
        
    });

    //se connecte au websocket pour récupérer les messages pour retirer de l'argent, 
    //les retransmets à la banque WEBSOCKET + MQTT
    socket.on('buttonClickedSub', function(amount){
        console.log('button clicked substraction: ' + amount);
        sendMqttMessage('banque/sub', 'sub;'+amount);
    });


    //se connecte au websocket pour récupérer les messages pour demander le compte 
    //en banque, les retransmets à la banque WEBSOCKET + MQTT
    socket.on('buttonClickedCheck', function(){
        console.log('Button clicked check');
        sendMqttMessage('banque/askCheck', 'check;');
    });

});
``` 

#### html
Ici on ajoute des évnements sur le "click des boutons". 
``` JS
<script src="/socket.io/socket.io.js"></script>
    <script>
        var socket = io.connect('ws://localhost:8080');
        socket.on('setBankAccount', function(data) {
            document.getElementById('compte_en_banque').innerHTML =  + data;
            console.log("Compte en banque : "+data);
        });
        //on récupère le nombre pour l'addition
        document.getElementById('add').addEventListener('click', function() {
            var number = document.getElementById('numberInput').value;
            //check if the input is a number not null
            if (number == "" || isNaN(number)) {
                alert("Please enter a valid number");
                return;
            }
            else {socket.emit('buttonClickedAdd', number);}
        });
        //on récupère le nombre pour la soustraction
        document.getElementById('remove').addEventListener('click', function() {
            var number = document.getElementById('numberInput').value;
            //check if the input is a number not null
            if (number == "" || isNaN(number)) {
                alert("Please enter a valid number");
                return;
            }
            else {socket.emit('buttonClickedSub', number);}
        });
        document.getElementById('check').addEventListener('click', function() {
            socket.emit('buttonClickedCheck');
        });

    </script>
``` 

#### Server JS
