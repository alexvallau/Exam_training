# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 14:26:43 2024

@author: Romain BRESSY
"""
import random
import time
import paho.mqtt.publish as publish

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "topic/jardin"

def simuler_capteurs():
    while True:
        temperature = round(random.uniform(10, 30), 2)
        humidite = round(random.uniform(30, 90), 2)
        # Créer un dictionnaire pour les données
        data = f"{temperature};{humidite}"
        # Convertir le dictionnaire en chaîne JSON
        publish.single(MQTT_TOPIC, data, hostname=MQTT_BROKER, port=MQTT_PORT)
        print(f"Message envoyé: {data}")
        time.sleep(5)
        
        # temperature = round(random.uniform(10, 30), 2)
        # humidite = round(random.uniform(30, 90), 2)
        # message = f"Temperature:{temperature},Humidite:{humidite}"
        # publish.single(MQTT_TOPIC, message, hostname=MQTT_BROKER, port=MQTT_PORT)
        # print(f"Message envoyé: {message}")
        # time.sleep(5)

# Pour démarrer la simulation dans un script séparé
if __name__ == "__main__":
    simuler_capteurs()
