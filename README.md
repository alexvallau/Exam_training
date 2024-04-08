## Flux de Messages entre `banque.py` et `server.js`

### Publication de Messages depuis `banque.py` :

1. Le fichier Python se connecte au courtier MQTT local (`localhost`) sur le port `1883` à l'aide de la bibliothèque `paho.mqtt.client`.
2. Les sujets MQTT sont définis comme suit :
    - `banque/add`: Pour ajouter des fonds au compte en banque.
    - `banque/sub`: Pour soustraire des fonds du compte en banque.
    - `banque/askCheck`: Pour demander le solde du compte en banque.
3. Lorsqu'un message est reçu sur l'un de ces sujets, la fonction `on_message` est déclenchée.
4. La fonction `on_message` analyse le message reçu et effectue les actions suivantes :
    - Si le message est de type "add", le montant spécifié dans le message est ajouté au solde du compte en banque.
    - Si le message est de type "sub", le montant spécifié dans le message est soustrait du solde du compte en banque.
    - Si le message est de type "askCheck", le script publie le solde actuel du compte en banque sur le sujet `compte_en_banque`.

### Réception de Messages dans `server.js` :

1. Le fichier JavaScript utilise Node.js avec les bibliothèques Express, Socket.IO et MQTT pour créer un serveur.
2. Le serveur s'abonne au sujet MQTT `compte_en_banque` pour recevoir les mises à jour du solde du compte en banque.
3. Lorsqu'un message est reçu sur ce sujet, la fonction de rappel `client.on('message')` est déclenchée.
4. Le serveur récupère le message reçu et met à jour la variable `compte_en_banque` avec la nouvelle valeur.
5. Le serveur utilise Socket.IO pour émettre le nouveau solde du compte en banque aux clients WebSocket connectés, mettant ainsi à jour l'interface utilisateur en temps réel.

