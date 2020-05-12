
#Importing the libraries for the Database and the Mqtt Client
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from influxdb import InfluxDBClient


Dataclient = InfluxDBClient(host='localhost',port=8086)
Dataclient.get_list_database()
#Creating and switching to our database
Dataclient.create_database('ProbaPractica')
Dataclient.switch_database('ProbaPractica')
time = 0
date = 0


#Checking if we have connected to the Mqtt server and subscribing to our topic
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe("training/device/Eduard-Epurica")
    #We publish this command to the topic so that the Raspberry pi will know to respond
    publish.single("training/device/Eduard-Epurica", "Get Time", hostname="mqtt.beia-telemetrie.ro")
#The instructions from when we recieve a publish message:
def on_message(client, userdata, msg):  
    print(msg.topic+" "+str(msg.payload))
	
    #If the length of the recieved message from the Raspberry Pi is 6 then we know that the message is the current time of the device
    if len(msg.payload) == 6:

        time = int(msg.payload)
        print("received time: ")
        #Creating a json_body1 containing the new information to be stored in the database
        json_body1 = [
            {
                "measurement": "Timpul",
                "tags": {
                    "User": "Eduard"
                },
                "fields": {
                    "Ora": time,
                }
             }
        ]
        print(time)
        #Writting the new information to the database
        Dataclient.write_points(json_body1)
#If the length of the recieved message from the Raspberry Pi is 9 then we know that the message is the current date of the device
    if len(msg.payload) == 8:

        date = int(msg.payload)
        print("received date: ")
        json_body1 = [
            {
                "measurement": "Date",
                "tags": {
                    "User": "Eduard"
                },
                "fields": {
                    "Data": date

                }
             }
        ]
        print(date)
        Dataclient.write_points(json_body1)


    if msg.payload == "Time and date sent":
        print("Received message will publish time and date to database")


#Creating an Mqtt client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
#Connecting our Mqtt client to the provided Mqtt server
client.connect("mqtt.beia-telemetrie.ro", 1883, 60)
client.loop_forever()
