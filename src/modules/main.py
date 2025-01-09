from microdot import Microdot, Response
from machine import Pin, I2C
import network
import ujson as json
import time

from ssd1306 import SSD1306_I2C

app = Microdot()
Response.default_content_type = "application/json"

i2c = I2C(0, scl=Pin(23), sda=Pin(22))
oled = SSD1306_I2C(128, 64, i2c)


sta = network.WLAN(network.STA_IF)
ap = network.WLAN(network.AP_IF)
# Configure a network on the configuration AP (RFC6598)
ap.ifconfig(("100.64.0.1", "255.255.255.0", "100.64.0.1", "100.64.0.1"))  # ip nm gw ns
ap_ssid = "ESP32-first-boot"
config_file = "config.json"


def load_config():
    print("Attempting to load configuration from flash")
    try:
        with open(config_file, "r") as f:
            return json.load(f)
    except OSError:
        return {}


def save_config(config):
    print("Writing configuration to flash")
    with open(config_file, "w") as f:
        json.dump(config, f)


def connect_to_wifi(config):
    ssid = config["ssid"]
    password = config["password"]

    sta.active(True)
    sta.connect(ssid, password)

    print(f"Connecting to {ssid}", end="")

    oled.fill(0)
    oled.text("Connecting to:", 0, 0)
    oled.text(ssid, 0, 22)
    oled.show()

    # Wait for connection
    for _ in range(20):  # Wait up to 10 seconds
        print(".", end="")
        if sta.isconnected():
            ip_address = sta.ifconfig()[0]
            oled.fill(0)
            oled.text("Connected:", 0, 0)
            oled.text(ip_address, 0, 22)
            oled.show()
            print("connected")
            return True
        time.sleep(0.5)

    print("failed")
    return False


# Load saved configuration
config = load_config()

if config.get("ssid"):
    connect_to_wifi(config)
else:
    # Set up AP mode for initial configuration
    ap.active(True)
    ap.config(essid=ap_ssid)
    print(f"Configuration AP {ap_ssid} ready")
    oled.fill(0)
    oled.text("AP available", 0, 0)
    oled.text(ap_ssid, 0, 22)
    oled.text("100.64.0.1", 0, 30)
    oled.show()


# API endpoint to configure Wi-Fi
@app.post("/api/configure")
def configure(request):
    try:
        data = request.json
        ssid = data.get("ssid")
        password = data.get("password")
    except Exception as _:
        return {
            "success": False,
            "message": "This endpoint expects valid JSON (did you set a correct request header?)",
        }, 400

    if not ssid or not password:
        return {"success": False, "message": "Missing ssid or password"}, 400

    # Save configuration and attempt to connect
    config["ssid"] = ssid
    config["password"] = password
    save_config(config)

    if connect_to_wifi(config):
        ap.active(False)
        ip_address = sta.ifconfig()[0]
        return {"success": True, "message": "Connection successful", "ip": ip_address}
    else:
        return {"success": False, "message": "Connection failed"}, 500


# API endpoint to display text on OLED
@app.post("/api/display")
def display(request):
    data = request.json
    text = data.get("text")

    if not text:
        return {"success": False, "message": "Missing text to display"}, 400

    oled.fill(0)
    oled.text(text[:16], 0, 0)  # Display first 16 characters on the first line
    if len(text) > 16:
        oled.text(text[16:32], 0, 10)  # Display next 16 characters on the second line
    oled.show()

    return {"success": True, "message": "Text displayed on OLED"}


# API endpoint to check Wi-Fi status
@app.get("/api/status")
def status(request):
    if sta.isconnected():
        return {"connected": True, "ip": sta.ifconfig()[0]}
    else:
        return {"connected": False, "message": "Not connected to WIFI"}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
