import cv2
import numpy as np

# Loading the Haar cascade files for face and eye
face_cascade = cv2.CascadeClassifier('haar_cascade_files/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haar_cascade_files/haarcascade_eye.xml')

# Checking if the face cascade file has been loaded correctly
if face_cascade.empty():
	raise IOError('Unable to load the face cascade classifier xml file')

# Checking if the eye cascade file has been loaded correctly
if eye_cascade.empty():
	raise IOError('Unable to load the eye cascade classifier xml file')

# Initializing the video capture object
cap = cv2.VideoCapture(0)

# Defining the scaling factor
ds_factor = 0.5

# Iteratation, until the user hits the 'Esc' key
while True:
    # Capturing the current frame
    _, frame = cap.read()

    # Resizing the frame
    frame = cv2.resize(frame, None, fx=ds_factor, fy=ds_factor, interpolation=cv2.INTER_AREA)

    # Converting to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Running the face detector on the grayscale image
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # For each face detected, running the eye detector
    for (x,y,w,h) in faces:
        # Extract the grayscale face ROI
        roi_gray = gray[y:y+h, x:x+w]

        # Extract the color face ROI
        roi_color = frame[y:y+h, x:x+w]

        # Running the eye detector on the grayscale ROI
        eyes = eye_cascade.detectMultiScale(roi_gray)

        # Below codw will draw circles around the eyes
        for (x_eye,y_eye,w_eye,h_eye) in eyes:
            center = (int(x_eye + 0.5*w_eye), int(y_eye + 0.5*h_eye))
            radius = int(0.5 * (w_eye + h_eye))
            color = (0, 255, 0)
            thickness = 3
            cv2.circle(roi_color, center, radius, color, thickness)

    # Displaying the output
    cv2.imshow('Eye Detector', frame)

    # Checking if the user hit the 'Esc' key
    c = cv2.waitKey(1)
    if c == 27:
        break

# Releasing the video capture object
cap.release()

# Closing all the windows
cv2.destroyAllWindows()
