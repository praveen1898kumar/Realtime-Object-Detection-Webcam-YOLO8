import cv2  # Import the OpenCV library
import pandas as pd  # Import the pandas library for data manipulation
import numpy as np  # Import the NumPy library for numerical computations
from ultralytics import YOLO  # Import the YOLO object detection model from Ultralytics

# Load the pre-trained YOLO model
model = YOLO('/Users/praveen18kumar/Downloads/CustomModel/best.pt')

# Open video capture from webcam (index 0)
cap = cv2.VideoCapture(0)

# Open the file containing class names and read its contents
my_file = open("/Users/praveen18kumar/Downloads/CustomModel/coco.names", "r")
data = my_file.read()

# Split the contents of the file by newline character to create a list of class names
class_list = data.split("\n") 

# Initialize a counter variable
count = 0

# Main loop for processing video frames
while True:    
    # Read a frame from the video capture
    ret, frame = cap.read()
    if not ret:
        break
    
    # Increment the counter
    count += 1
    
    # Process every third frame only
    if count % 3 != 0:
        continue
    
    # Resize the frame to a specified size
    frame = cv2.resize(frame, (1020, 500))
    
    # Flip the frame horizontally
    frame = cv2.flip(frame, 1)
    
    # Perform object detection using the YOLO model
    results = model.predict(frame)

    # Extract bounding boxes and class labels from the detection results
    a = results[0].boxes.boxes
    px = pd.DataFrame(a).astype("float")
    
    # Loop over each detected object
    for index, row in px.iterrows():
        x1 = int(row[0])  # Top-left x-coordinate of the bounding box
        y1 = int(row[1])  # Top-left y-coordinate of the bounding box
        x2 = int(row[2])  # Bottom-right x-coordinate of the bounding box
        y2 = int(row[3])  # Bottom-right y-coordinate of the bounding box
        d = int(row[5])   # Class label index
        c = class_list[d]  # Class label
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Draw bounding box
        cv2.putText(frame, c, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)  # Put text with class name
   
    # Display the processed frame
    cv2.imshow("FRAME", frame)
    
    # Check for key press; If 'Esc' key is pressed, break out of the loop
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
