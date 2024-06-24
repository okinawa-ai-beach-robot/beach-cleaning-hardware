from beachbot import manipulators
from beachbot import utils
import time


def main():
    kp = 1.0
    ki = 0.0
    kd = 0.0
    setpoint_x = 0.0
    setpoint_y = 0.0
    pid_controller = manipulators.drive.PIDController(
        kp, ki, kd, setpoint_x, setpoint_y
    )

    # Example Motor setup and initialization
    # TODO get default pin values from some beachbot.util definition
    motor_left = manipulators.drive.Motor(pwm_pin=18, in1=23, in2=24, frequency_hz=100)
    motor_right = manipulators.drive.Motor(pwm_pin=25, in1=8, in2=7, frequency_hz=100)

    # Main loop
    while True:
        # Get the center of the 'trash_easy' object
        detections = model(img)
        center = utils.get_highest_confidence_trash_easy_center(detections)

        # Check for error
        if center.error:
            print("Error:", center.error)
            continue

        # Get PID output
        pid_output_x, pid_output_y = pid_controller.get_output(center.x, center.y)
        print("PID output:", pid_output_x, pid_output_y)

        # Map PID output to motor speeds (-100 to 100)
        speed_left = pid_output_x
        speed_right = pid_output_x

        # Drive motors
        motor_left.change_speed(speed_left)
        motor_right.change_speed(speed_right)

        time.sleep(0.1)  # Adjust as needed for your application


if __name__ == "__main__":
    main()
