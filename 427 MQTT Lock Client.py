import paho.mqtt.client as mqtt
import time

def on_message(inclient, userdata, message):
    decoded_message = message.payload.decode('utf-8')
    print(decoded_message)


broker_address = "127.0.0.1"
client = mqtt.Client('lock_client')
client.on_message = on_message
client.connect(broker_address)

client.loop_start()
client.subscribe("lock/status")
print("Connected to Server\n")

while True:
    userInput = input("Please enter a command.\n\t"
                      "1.) Toggle Lock\n\t"
                      "2.) Toggle Temporary Password\n\t"
                      "3.) Close Client\n")

    if userInput == "1":
        payload = "toggleLock "
        userInput = input("Please enter the password.\n")
        payload += userInput
        client.publish("lock/input", payload)
        time.sleep(2)
        continue

    if userInput == "2":
        payload = "toggleTempPassword "
        userInput = input("Please enter the password.\n")
        payload += userInput
        client.publish("lock/input", payload)
        time.sleep(2)
        continue

    if userInput == "3":
        print("Closing Connection\n")
        client.disconnect()
        break

    print("Command not recognized. Please enter only 1, 2, or 3.\n")
client.loop_stop()

