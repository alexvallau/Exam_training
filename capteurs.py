#owkring
import random
import time
import paho.mqtt.client as mqtt




def publier_donnees():
    temperature = round(random.uniform(-10, 50), 1)
    humidite = round(random.uniform(0, 100), 1)

    print(f"Température: {temperature}")
    print(f"Humidité: {humidite}")

    return temperature,humidite


def on_message(client, userdata, message): # définit la fonction de rappel pour gérer les messages reçus
    print(message.topic, message.payload)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2) # initialise le client MQTT
client.connect("localhost", 1883, 60) # connecte le client MQTT à un broker Mosquitto
url = "http://localhost:3000"

while True:
    temperature, humidite = publier_donnees()
    client.publish("jardin", str(humidite)+";"+str(temperature))
    #client.publish("jardin", str(temperature)) # publie un message sur le topic "jardin"
    #client.publish("jardin", str(humidite))
    time.sleep(5)
