import network
import time
from umqtt.simple import MQTTClient
from machine import Pin, ADC, reset

# WiFi parametri
wifi_ssid = 'Lab220'
wifi_password = 'lab220lozinka'

# MQTT parametri
mqtt_server = '10.12.20.130'
client_id = 'pico_client'
topic_set_temp = b'control/set_temperature'
topic_relay = b'control/relay'
topic_temp_report = b'sensor/temperature'
topic_relay_status = b'relay/status'

# Inicijalizacija releja i senzora
relay = Pin(15, Pin.OUT)
relay.value(0)  # Relej isključen na početku

lm35 = ADC(Pin(28))

set_temperature = 25.0
hysteresis = 2.0  # histereza u stepenima
relay_on = False  # stanje releja

# Funkcija za povezivanje na WiFi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Povezivanje na mrežu...')
        wlan.connect(wifi_ssid, wifi_password)
        while not wlan.isconnected():
            time.sleep(0.5)
    print('Mreža povezana. IP:', wlan.ifconfig()[0])

# Funkcija za provjeru WiFi konekcije
def ensure_wifi():
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        print("WiFi veza izgubljena. Resetujem...")
        time.sleep(2)
        reset()

# MQTT callback funkcija
def sub_callback(topic, msg):
    global set_temperature
    print('Primljena MQTT poruka:', topic, msg)

    if topic == topic_set_temp:
        try:
            set_temperature = float(msg)
            print('Podesena ciljna temperatura:', set_temperature)
        except:
            print("Greška pri parsiranju temperature.")

    elif topic == topic_relay:
        if msg == b'ON':
            relay.value(1)
            client.publish(topic_relay_status, b'ON')
        elif msg == b'OFF':
            relay.value(0)
            client.publish(topic_relay_status, b'OFF')

# Očitavanje temperature sa LM35 senzora
def read_temperature():
    try:
        raw = lm35.read_u16()
        voltage = raw * 3.3 / 65535
        temp_c = voltage * 100
        return temp_c
    except Exception as e:
        print('Greška pri očitavanju sa LM35:', e)
        return None

connect_wifi()
time.sleep(2)  

# Povezivanje na MQTT
try:
    client = MQTTClient(client_id, mqtt_server)
    client.set_callback(sub_callback)
    client.connect()
    client.subscribe(topic_set_temp)
    client.subscribe(topic_relay)
    print('MQTT povezan sa brokerom na', mqtt_server)
except OSError as e:
    print('MQTT konekcija neuspešna:', e)
    time.sleep(5)
    reset()


while True:
    ensure_wifi()
    try:
        client.check_msg()
        temp = read_temperature()
        if temp is not None:
            print(f'Temp: {temp:.2f} °C | Cilj: {set_temperature} °C')
            client.publish(topic_temp_report, str(temp))

            # Histereza
            if relay_on:
                if temp >= set_temperature + hysteresis:
                    relay.value(0)
                    client.publish(topic_relay_status, b'OFF')
                    relay_on = False
            else:
                if temp <= set_temperature - hysteresis:
                    relay.value(1)
                    client.publish(topic_relay_status, b'ON')
                    relay_on = True

        else:
            print("Preskačem jer temperatura nije očitana.")
    except OSError as e:
        print('Greška u MQTT komunikaciji:', e)
        time.sleep(3)
        reset()

    time.sleep(5)