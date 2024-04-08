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


### Flux de message MQTT

#### Server JS
