## Flux de Messages entre `banque.py` et `server.js`

### Publication de Messages depuis `banque.py` :

1. Le fichier Python utilise la bibliothèque `paho.mqtt.client` pour se connecter à un courtier MQTT local (`localhost`) sur le port `1883`.
2. Il définit plusieurs variables telles que `topicAdd`, `topicSub`, `topicPublisher`, etc., qui représentent les différents sujets MQTT.
3. Le script Python utilise une fonction `on_message` pour traiter les messages reçus. Lorsqu'un message est reçu sur les sujets `banque/add`, `banque/sub`, ou `banque/askCheck`, il est analysé pour déterminer l'action à effectuer (ajouter, soustraire ou vérifier le solde).
4. En fonction de l'action identifiée dans le message, le montant est ajouté ou soustrait du solde actuel du compte en banque.
5. Si le message est de type "check", le script Python répond en publiant le solde actuel du compte en banque sur le sujet `compte_en_banque`.

### Réception de Messages dans `server.js` :

1. Le fichier JavaScript (`server.js`) crée un serveur HTTP à l'aide de Node.js et Express, et un serveur WebSocket à l'aide de Socket.IO.
2. Il se connecte également au courtier MQTT local en utilisant la bibliothèque `mqtt`.
3. Lorsque le serveur Node.js est démarré, il s'abonne au sujet `compte_en_banque` pour recevoir les mises à jour du solde du compte en banque.
4. Lorsqu'un message est reçu sur le sujet `compte_en_banque`, le serveur Node.js met à jour la variable `compte_en_banque` avec la nouvelle valeur reçue.
5. Le serveur Node.js utilise Socket.IO pour émettre le nouveau solde du compte en banque aux clients WebSocket connectés, ce qui met à jour l'interface utilisateur en temps réel.

