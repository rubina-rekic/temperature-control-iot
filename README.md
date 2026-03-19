# Temperature Control IoT 🌡️

A two-position (on/off) temperature regulation system built with a Raspberry Pi Pico microcontroller, Flask web interface, and MQTT communication protocol. The system automatically controls a relay based on measured vs. target temperature, with real-time monitoring and control via a local network web interface.

---

## How It Works

```
LM35 Sensor → Raspberry Pi Pico → MQTT Broker → Flask Web App
                     ↓                                ↓
                  Relay                        Web Interface
               (heater on/off)            (monitor & control)
```

1. The **LM35 sensor** continuously measures room temperature
2. **Raspberry Pi Pico** reads the sensor and applies two-position (hysteresis) control logic
3. Temperature data and relay status are sent via **MQTT** to a central Raspberry Pi
4. A **Flask web app** displays live data and allows the user to set target temperature or manually control the relay

---

## Features

- ✅ Automatic relay control based on target temperature with hysteresis
- ✅ Real-time temperature monitoring via web interface
- ✅ Set target temperature through the web UI
- ✅ Manual relay override (ON/OFF) via web UI
- ✅ MQTT-based communication between microcontroller and server
- ✅ Auto-reconnect on WiFi or MQTT connection loss

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Microcontroller | Raspberry Pi Pico (MicroPython) |
| Temperature Sensor | LM35 (analog) |
| Relay Control | GPIO Pin (Raspberry Pi Pico) |
| Communication | MQTT (Mosquitto broker) |
| Backend | Python, Flask |
| Frontend | HTML, CSS (Jinja2 templates) |
| Server | Raspberry Pi |

---

## Project Structure

```
temperature-control-iot/
├── pico/
│   └── main.py              # MicroPython code for Raspberry Pi Pico
├── flask/
│   ├── app.py               # Flask backend + MQTT client
│   └── templates/
│       └── index.html       # Web interface
├── docs/
│   └── specifikacija.pdf    # Project specification document
├── requirements.txt         # Python dependencies
└── README.md
```

---

## Getting Started

### Prerequisites
- Raspberry Pi with Mosquitto MQTT broker installed
- Raspberry Pi Pico with MicroPython firmware
- Python 3.x
- LM35 temperature sensor + relay module

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/rubina-rekic/temperature-control-iot.git
cd temperature-control-iot
```

**2. Install Python dependencies**
```bash
pip install -r requirements.txt
```

**3. Configure MQTT broker IP**

In both `pico/main.py` and `flask/app.py`, update the broker IP:
```python
MQTT_BROKER = "YOUR_RASPBERRY_PI_IP"
```

**4. Upload Pico code**

Open `pico/main.py` in Thonny IDE and upload it to the Raspberry Pi Pico.

**5. Run the Flask app**
```bash
cd flask
python app.py
```

Open your browser at `http://YOUR_RASPBERRY_PI_IP:5000`

---

## MQTT Topics

| Topic | Direction | Description |
|-------|-----------|-------------|
| `sensor/temperature` | Pico → Flask | Current measured temperature |
| `relay/status` | Pico → Flask | Current relay state (ON/OFF) |
| `control/set_temperature` | Flask → Pico | Set new target temperature |
| `control/relay` | Flask → Pico | Manual relay command (ON/OFF) |

---

## Team

- Rubina Rekić
- Irma Topčagić
- Asja Festa
- Irma Lemeš

*University project — Electrical Engineering Faculty, Sarajevo, June 2025*
