from yolo5 import Detections
import pandas as pd
from typing import Tuple, Optional


class CenterCoordinates:
    def __init__(
        self,
        x: Optional[float] = None,
        y: Optional[float] = None,
        error: Optional[str] = None,
    ):
        self.x = x
        self.y = y
        self.error = error


class PIDController:
    def __init__(
        self, kp: float, ki: float, kd: float, setpoint_x: float, setpoint_y: float
    ):
        self.kp = kp
        # self.ki = ki
        # self.kd = kd
        self.setpoint_x = setpoint_x
        self.setpoint_y = setpoint_y
        # self.prev_error_x = 0
        # self.prev_error_y = 0
        # self.integral_x = 0
        # self.integral_y = 0

    def get_output(self, x: float, y: float) -> Tuple[int, int]:
        error_x = self.setpoint_x - x
        error_y = self.setpoint_y - y

        # self.integral_x += error_x
        # self.integral_y += error_y

        # derivative_x = error_x - self.prev_error_x
        # derivative_y = error_y - self.prev_error_y

        output_x = (
            self.kp * error_x
        )  # + self.ki * self.integral_x + self.kd * derivative_x
        output_y = (
            self.kp * error_y
        )  # + self.ki * self.integral_y + self.kd * derivative_y

        # self.prev_error_x = error_x
        # self.prev_error_y = error_y

        # Normalize output to -100 to 100
        output_x = max(min(output_x, 100), -100)
        output_y = max(min(output_y, 100), -100)

        return int(output_x), int(output_y)


def get_highest_confidence_trash_easy_center(
    detections: "Detections",
) -> CenterCoordinates:
    """
    Get the xcenter and ycenter of the bounding box for the highest confidence "trash_easy" prediction.

    Args:
    - detections ('Detections'): An instance of the Detections class containing the object detection results.

    Returns:
    - CenterCoordinates: An instance of the CenterCoordinates class containing the xcenter and ycenter coordinates,
                         or an error message if no detections are found.
    """
    if len(detections.pred) == 0:
        return CenterCoordinates(error="No detections found.")

    # Get pandas dataframe for xyxy predictions
    df: pd.DataFrame = detections.pandas().xyxy[0]

    # Filter predictions by class name "trash_easy"
    trash_easy_df: pd.DataFrame = df[df["name"] == "trash_easy"]

    if len(trash_easy_df) == 0:
        return CenterCoordinates(error="No 'trash_easy' detections found.")

    # Get the row with the highest confidence
    highest_confidence_row: pd.Series = trash_easy_df.loc[
        trash_easy_df["confidence"].idxmax()
    ]

    # Get xcenter and ycenter
    xcenter: float = (
        highest_confidence_row["xmin"] + highest_confidence_row["xmax"]
    ) / 2
    ycenter: float = (
        highest_confidence_row["ymin"] + highest_confidence_row["ymax"]
    ) / 2

    return CenterCoordinates(xcenter, ycenter)
