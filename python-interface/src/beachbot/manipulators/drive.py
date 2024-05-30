import time
import math

try:
    import Jetson.GPIO as GPIO
except ModuleNotFoundError as ex:
    print(
        "Jetson GPIO library not installed or not available!\nMotor interface may not be available!"
    )



class Motor:
    def __init__(self, pwm_pin: int, in1: int, in2: int, frequency_hz: int) -> None:
        self.pwm_pin: int = pwm_pin
        self.in1: int = in1
        self.in2: int = in2
        self.frequency_hz: int = frequency_hz
        self.duty_cycle_percent: int = (
            0  # Initialized to 0, and int can hold -100 to 100 inclusively
        )
        GPIO.setup([in1, in2], GPIO.OUT, initial=GPIO.LOW)
        # set pin as an output pin with optional initial state of LOW
        GPIO.setup(self.pwm_pin, GPIO.OUT, initial=GPIO.LOW)
        # p1 is a PWM object.
        self.pwm = GPIO.PWM(self.pwm_pin, self.frequency_hz)
        self.pwm.start(self.duty_cycle_percent)

    def change_speed(self, speed: int) -> None:
        """
        Change the motor speed.

        Args:
            speed (int): Speed of the motor, ranging from -100 to 100.
                         Negative values represent reverse motion,
                         positive values represent forward motion,
                         and zero stops the motor.
        """
        if not -100 <= speed <= 100:
            raise ValueError(
                f"Speed must be between -100 and 100 inclusive. Received: {speed}"
            )

        self.duty_cycle_percent = abs(speed)

        if speed > 0:
            GPIO.output(self.in1, GPIO.HIGH)
            GPIO.output(self.in2, GPIO.LOW)
        elif speed < 0:
            GPIO.output(self.in1, GPIO.LOW)
            GPIO.output(self.in2, GPIO.HIGH)
        else:
            # Brake: INx1 = LOW, INx2 = LOW
            GPIO.output(self.in1, GPIO.LOW)
            GPIO.output(self.in2, GPIO.LOW)

        self.pwm.ChangeDutyCycle(self.duty_cycle_percent)

    def turn_off(self) -> None:
        self.pwm.stop()
