from flask import Flask, render_template, redirect, url_for, request, jsonify
from save_to_db import save_pin, get_reserved_pins
import json
import serial
import time

app = Flask(__name__)
arduino = serial.Serial('COM4', 9600, timeout=5)
time.sleep(2)

arduino.reset_input_buffer()
arduino.reset_output_buffer()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/fetch_pins")
def fetch_pins():
    update_pins()
    arduino.write(b'A')
    pins = arduino.readline().decode().strip()
    data = json.loads(pins)
    print("Pins", data["available_pins"])
    return jsonify(data)

@app.route("/led_action", methods=["POST"])
def led_action():
    data = request.get_json()
    pin = data.get("pin")
    save_pin(pin)
    command = f"C{pin}\n".encode()
    arduino.write(command)
    return jsonify(data)

@app.route("/off")
def off():
    arduino.write(b'B')
    current_pins = arduino.readline().decode().strip()
    data = json.loads(current_pins)
    return render_template('current-pins.html', pins = data["reserved_pins"])

@app.route("/turn_off", methods=["POST"])
def turn_off():
    data = request.get_json("pin")
    pin = data.get("pin")
    command = f"O{pin}\n".encode()
    arduino.write(command)
    return redirect(url_for('off'))

def update_pins():
    try:
        reserved_pin_list = get_reserved_pins()
        reserved_pins = [int(d['pin_number']) for d in reserved_pin_list]
        pins_list = json.dumps(reserved_pins)
        command = f"U{pins_list}\n".encode()
        arduino.write(command)
        return {"status" : "updated"}
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error updated_pins : {e}")
        return None

if __name__ == "__main__":
    try:
        app.run(debug=True, use_reloader=False)
    finally:
        if arduino and arduino.is_open:
            arduino.close()
            print("🔌 Arduino connection closed cleanly.")