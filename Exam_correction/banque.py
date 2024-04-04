import paho.mqtt.client as mqtt

# MQTT broker details
broker_address = "localhost"
broker_port = 1883
topic = "banque"
topicAdd = "banque/add"
topicSub = "banque/sub"
topicPublisher= "banque/askCheck"
topics = [topicAdd, topicSub, topic, topicPublisher]
topicToPublish = "compte_en_banque"


compte_en_banque = 0
# In your on_publish callback
def on_publish(client, userdata, mid, reason_code, properties):
    # reason_code and properties will only be present in MQTTv5. It's always unset in MQTTv3
    try:
        userdata.remove(mid)
    except KeyError:
        print("on_publish() is called with a mid not present in unacked_publish")
# Callback function for when a message is received
#def on_message(client, userdata, message):
#    print("Received message: " + str(message.payload.decode()))

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
    elif message[0] == "check":
        print("Demande de solde")
        msg_info=mqttc.publish("compte_en_banque", str(compte_en_banque), qos=0)
        unacked_publish.add(msg_info.mid)
        msg_info.wait_for_publish()
        
        
    print("Compte en banque: ", compte_en_banque)
   


unacked_publish = set()
# Create MQTT client instance
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)


mqttc.user_data_set(unacked_publish)
mqttc.connect("localhost")
mqttc.loop_start()

# Set callback function for message reception
client.on_message = on_message
mqttc.on_publish = on_publish



# Connect to MQTT broker
client.connect(broker_address, broker_port)

# Subscribe to the topic
#client.subscribe(topic)
for topic in topics:
    client.subscribe(topic)
# Start the MQTT loop to receive messages
client.loop_start()

# Keep the client running until interrupted
try:
    while True:
        pass
except KeyboardInterrupt:
    pass

# Disconnect from MQTT broker
client.loop_stop()
client.disconnect()