import paho.mqtt.client as mqtt
import time

LockState = False
TempPasswordState = False
Password = "12345"
TempPassword = "54321"


def togglelock(payload):
    global LockState
    global TempPasswordState

    decoded_payload = payload.decode('utf-8')
    if "12345" in decoded_payload:
        LockState = not LockState
        lock = open("lock.txt", "w")
        if LockState:
            client.publish("lock/status", "Lock Enabled")
            print("Lock Enabled")
            lock.write("1")
        else:
            client.publish("lock/status", "Lock Disabled")
            print("Lock Disabled")
            lock.write("0")
        return

    if "54321" in decoded_payload:
        if TempPasswordState:
            LockState = not LockState
            lock = open("lock.txt", "w")
            if LockState:
                client.publish("lock/status", "Lock Enabled")
                print("Lock Enabled")
                lock.write("1")
            else:
                client.publish("lock/status", "Lock Disabled")
                print("Lock Disabled")
                lock.write("0")
            TempPasswordState = False
            client.publish("lock/status", "Temporary Password Disabled")
            print("Temporary Password Disabled")
        return

    client.publish("lock/status", "Password not recognized")


def toggletemppassword(payload):
    global TempPasswordState
    decoded_payload = payload.decode('utf-8')
    if "12345" in decoded_payload:
        TempPasswordState = not TempPasswordState
        if TempPasswordState:
            client.publish("lock/status", "Temporary Password Enabled\nTemporary Password: %s" % TempPassword)
            print("Temporary Password Enabled")
        else:
            client.publish("lock/status", "Temporary Password Disabled")
            print("Temporary Password Disabled")
        return

    client.publish("lock/status", "Password not recognized")


def on_message_call(inclient, userdata, message):
    print("Messaged Received: %s %s" % (message.topic, message.payload.decode('utf-8')))
    decoded_payload = message.payload.decode('utf-8')
    if "toggleLock" in decoded_payload:
        togglelock(message.payload)
        return
    if "toggleTempPassword" in decoded_payload:
        toggletemppassword(message.payload)
        return
    client.publish("lock/status", "Command not recognized.")


broker_address = "127.0.0.1"
client = mqtt.Client('lock_server')
client.on_message = on_message_call
client.will_set("lock/status", "Lock has been disconnected.", 1, False)
client.connect(broker_address)

client.loop_start()
client.subscribe("lock/input")
client.publish("lock/status", "Lock Connected")

time.sleep(60)
client.disconnect()
client.loop_stop()
