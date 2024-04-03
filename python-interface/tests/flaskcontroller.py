from flask import Flask, render_template, request
from beachbot.manipulators import Motor
import Jetson.GPIO as GPIO
import time

app = Flask(__name__)

pwm_pins = [32, 33]
gpio_pins = [7, 15, 29, 31]
_frequency_hz = 50

GPIO.setmode(GPIO.BOARD)

motor1 = Motor(pwm_pins[0], gpio_pins[0], gpio_pins[1], _frequency_hz)
motor2 = Motor(pwm_pins[1], gpio_pins[2], gpio_pins[3], _frequency_hz)

sleep_time = 0.1


def cleanup():
    GPIO.cleanup()
    motor1.cleanup()
    motor2.cleanup()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/stop", methods=["POST"])
def stop():
    # Call your function here, e.g.,
    motor1.change_speed(0)
    motor2.change_speed(0)
    return f"Speed changed to {0}"


@app.route("/left", methods=["POST"])
def left():
    speed = request.form.get("speed")
    # Call your function here, e.g.,
    motor1.change_speed(-int(speed))
    motor2.change_speed(int(speed))
    return f"Speed changed to {speed}"


@app.route("/right", methods=["POST"])
def right():
    speed = request.form.get("speed")
    # Call your function here, e.g.,
    motor1.change_speed(int(speed))
    motor2.change_speed(-int(speed))
    return f"Speed changed to {speed}"


@app.route("/forward", methods=["POST"])
def forward():
    speed = request.form.get("speed")
    # Call your function here, e.g.,
    motor1.change_speed(int(speed))
    motor2.change_speed(int(speed))
    return f"Speed changed to {speed}"


@app.route("/backward", methods=["POST"])
def backward():
    speed = request.form.get("speed")
    # Call your function here, e.g.,
    motor1.change_speed(-int(speed))
    motor2.change_speed(-int(speed))
    return f"Speed changed to {speed}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
