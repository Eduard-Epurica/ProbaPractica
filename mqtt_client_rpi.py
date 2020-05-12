#Importing the necessary libraries for the Mqtt client
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
#from influxdb import InfluxDBClient
import datetime

#Storing the current time and date on the device which represents the information to be sent to the mqtt server
now = datetime.datetime.now()
print("Curent date and time: ")
print(now.strftime("%Y-%m-%d %H:%M:%S"))


#Connecting automatically to the topic of our choosing
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("training/device/Eduard-Epurica")
#Checking if we have connected to the mqtt server and subscribing to our topic
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
#If we receive a request from the PC for the time, we publish the information to the Mqtt topic
    if msg.payload == "Get Time":
        now = datetime.datetime.now()
        date=now.strftime("%Y%m%d")
        time=now.strftime("%H%M%S")
        print("Received message will publish time and date")
        publish.single("training/device/Eduard-Epurica", date, hostname="mqtt.beia-telemetrie.ro")
        publish.single("training/device/Eduard-Epurica", time, hostname="mqtt.beia-telemetrie.ro")
        publish.single("training/device/Eduard-Epurica", "Time and date sent", hostname="mqtt.beia-telemetrie.ro")
        
     
# Create an MQTT client and connecting to the provided mqtt server
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
 
client.connect("mqtt.beia-telemetrie.ro", 1883, 60)
 

client.loop_forever()