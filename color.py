import cv2
import numpy as np

# Function to detect colors in an image
def detect_colors(image, color_to_detect):
    # Convert the image to the HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds for the colors you want to detect (in HSV format)
    if color_to_detect == "red":
        lower_color = np.array([0, 100, 100])     # Lower bound for red color
        upper_color = np.array([10, 255, 255])    # Upper bound for red color
        color_name = "Red"
        color_bgr = (0, 0, 255)  # Red color in BGR format
    elif color_to_detect == "blue":
        lower_color = np.array([100, 100, 100])   # Lower bound for blue color
        upper_color = np.array([140, 255, 255])  # Upper bound for blue color
        color_name = "Blue"
        color_bgr = (255, 0, 0)  # Blue color in BGR format
    elif color_to_detect == "green":
        lower_color = np.array([40, 40, 40])    # Lower bound for green color
        upper_color = np.array([80, 255, 255])  # Upper bound for green color
        color_name = "Green"
        color_bgr = (0, 255, 0)  # Green color in BGR format
    elif color_to_detect == "yellow":
        lower_color = np.array([20, 100, 100])  # Lower bound for yellow color
        upper_color = np.array([30, 255, 255])  # Upper bound for yellow color
        color_name = "Yellow"
        color_bgr = (0, 255, 255)  # Yellow color in BGR format
    else:
        return image  # Return the original image if an unsupported color is specified

    # Create a mask for the specified color
    mask = cv2.inRange(hsv_image, lower_color, upper_color)

    # Find contours in the color mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw bounding rectangles around the detected objects of the specified color
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(image, (x, y), (x + w, y + h), color_bgr, 2)
        
    # Add the detected color text overlay
    cv2.putText(image, f"Detecting Color: {color_name}", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, color_bgr, 2)

    return image

# Capture video from the default camera (you can specify a different camera index if needed)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        break
    
    keys_overlay = "1: Red, 2: Blue, 3: Green, 4: Yellow "
    cv2.putText(frame, keys_overlay, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, .7, (0, 100, 255), 2)
    cv2.putText(frame, " Hold Number to Detect", (40, 60), cv2.FONT_HERSHEY_SIMPLEX, .8, (0, 100, 255), 2)
    cv2.putText(frame, " Press q to quit", (100, 550), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 100, 255), 2)
    # Read the user input key
    key = cv2.waitKey(1) & 0xFF

    # Detect colors based on user input
    if key == ord('1'):
        result_frame = detect_colors(frame, "red")
    elif key == ord('2'):
        result_frame = detect_colors(frame, "blue")
    elif key == ord('3'):
        result_frame = detect_colors(frame, "green")
    elif key == ord('4'):
        result_frame = detect_colors(frame, "yellow")
    else:
        result_frame = frame  # Display the original frame if no valid input is provided

    # Display the result
    cv2.imshow("Color Detection", result_frame)

    # Exit the loop when the 'q' key is pressed
    if key == ord('q'):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
