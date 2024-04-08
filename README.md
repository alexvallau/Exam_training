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
A la fin de cette étape, on sera capable de cliquer sur les boutons de la page web. Ces boutons seront envoyés à notre serveur javascript. Quand j'appuie sur ajouter ou retirer, le contenu du champs "number" sera envoyé au serveur, qui le traitera.
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

## Coder l'intéraction entre notre serveur JS(publisher) et notre code python (subscriber).
Maintenant que l'on a récupéré les bouton, à savoir que l'utilisateur appuie sur +/- ou "consulter", il faut maintenant les envoyer à la banque, afin que l'on puisse ajouter de l'argent sur un solde, retirer de l'argent ou tout simplement consulter le solde.
#### Server.js
On commence par coder une fonction qui va prendre en argument un topic et un message.
```js
//Fonction qui envoie un message mqtt à la banque
function sendMqttMessage(topic, message){
    var client = mqtt.connect('mqtt://localhost');
    client.on('connect', function(){
        client.publish(topic, message);
        client.end();
    });
}
```

Cette fonction sera ensuite utilisée dans "io.on"(fonction vue précédemment):
ou l'on publiera les messages de type:
``` js
sendMqttMessage('banque/add', 'add;'+amount);
sendMqttMessage('banque/sub', 'sub;'+amount);
sendMqttMessage('banque/askCheck', 'check;');
``` 
#### banque.py
Dans ce fichier, on va coder le fait de: 
* S'abonner à un topic
* traiter des messages du type add;30 ou sub;30

  
Concrètement ici, notre code ne fait que recevoir des messages du type ajouter ou retirer, afin d'ajouter le nombre à une variable globale "compte_en_banque". Il ne renvoit encore rien à notre serveur js

``` python
import paho.mqtt.client as mqtt

# Tous les topics/ports/adresses utiles, pour mtnt ou le turfu
broker_address = "localhost"
broker_port = 1883
topic = "banque"
topicAdd = "banque/add"
topicSub = "banque/sub"
topicPublisher= "banque/askCheck"
topics = [topicAdd, topicSub, topic, topicPublisher]
topicToPublish = "compte_en_banque"
compte_en_banque = 0
#Fonction qui récupère le message, split ";" et effectue l'opération
def on_message(client, userdata, message):
    global compte_en_banque
    message = message.payload.decode()
    message = message.split(";")
    print("Message reçu:: ", message)
    if message[0] == "add":
        compte_en_banque += int(message[1])
    elif message[0] == "sub":
        compte_en_banque -= int(message[1])

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
# Connect to MQTT broker
client.connect(broker_address, broker_port)
# Subscribe to the topic
#client.subscribe(topic)
for topic in topics:
    client.subscribe(topic)
# Start the MQTT loop to receive messages
client.loop_start()
client.on_message = on_message

# Keep the client running until interrupted
try:
    while True:
        pass
except KeyboardInterrupt:
    pass
# Disconnect from MQTT broker
client.loop_stop()
client.disconnect()
```
## Intéraction entre banque.py(publisher) et server.js(suscriber)
On récapitule:
* Ma page web communique avec mon serveur JS, on peut récupérer des sommes d'argent et les ajouter/ retirer de notre compte en banque
* Il faut maintenant que notre client puisse récupérer son compte en banque sur sa page web.
* Pour cela il faut que notre banque.py, puisse communiquer la variable ``` compte_en_banque```
* Il faut donc que banque.py devienne un publisher et server.js un subcriber.
  
