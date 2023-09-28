import cv2
from PIL import Image
from util import get_limits
import numpy as np

# Define a dictionary to map color names to BGR values
color_dict = {
    "blue": [255, 0, 0],
    "red": [0, 0, 255],
    "green": [0, 255, 0],
    "yellow": [0, 255, 255]
}

col = "blue"  # Change this to the desired color name

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()

    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Get the BGR values based on the color name
    if col in color_dict:
        color_bgr = color_dict[col]
    else:
        color_bgr = [0, 0, 0]  # Default to black if color is not recognized

    lowerLimit, upperLimit = get_limits(color=color_bgr)

    mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)

    mask_ = Image.fromarray(mask)

    bbox = mask_.getbbox()

    if bbox is not None:
        x1, y1, x2, y2 = bbox

        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
        cv2.putText(frame, f"Detected Color: {col}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

