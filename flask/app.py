from flask import Flask, render_template, request, redirect
import paho.mqtt.client as mqtt

app = Flask(__name__)

MQTT_BROKER = "10.12.20.130"
MQTT_PORT = 1883

current_temperature = None
relay_status = "OFF"
set_temperature = 25.0

client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("sensor/temperature")
    client.subscribe("relay/status")

def on_message(client, userdata, msg):
    global current_temperature, relay_status
    topic = msg.topic
    payload = msg.payload.decode()
    if topic == "sensor/temperature":
        try:
            current_temperature = float(payload)
        except ValueError:
            print("Nevažeća temperatura:", payload)
    elif topic == "relay/status":
        relay_status = payload

client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

@app.route("/", methods=["GET", "POST"])
def index():
    global set_temperature
    if request.method == "POST":
        if "new_temp" in request.form:
            try:
                new_temp = float(request.form["new_temp"])
                set_temperature = new_temp
                client.publish("control/set_temperature", str(new_temp))
            except ValueError:
                print("Neispravan unos temperature.")
        elif "relay_cmd" in request.form:
            cmd = request.form["relay_cmd"]
            if cmd in ["ON", "OFF"]:
                client.publish("control/relay", cmd)
        return redirect("/")

    return render_template(
        "index.html",
        temperature=current_temperature,
        relay=relay_status,
        set_temp=set_temperature
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)