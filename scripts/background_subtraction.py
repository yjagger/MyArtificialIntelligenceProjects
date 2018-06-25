import cv2
import numpy as np

#function to get the current frame from the webcam
def get_frame(cap, scaling_factor):
    # Read the current frame from the video capture object
    _, frame = cap.read()

    # Resizing the image
    frame = cv2.resize(frame, None, fx=scaling_factor, 
            fy=scaling_factor, interpolation=cv2.INTER_AREA)

    return frame

if __name__=='__main__':
    # Defining the video capture object
    cap = cv2.VideoCapture(0)

    # Define the background subtractor object
    bg_subtractor = cv2.createBackgroundSubtractorMOG2()
     
    # Define the number of previous frames to use to learn. 
    # play with this parameter, which will change the learning rate and see how it affects the output 
    history = 100
    
    
    learning_rate = 1.0/history

    # Keep reading the frames from the webcam  untill ESC key is pressed
    while True:
        # Grabbing the current frame
        frame = get_frame(cap, 0.5)

        # mask computation 
        mask = bg_subtractor.apply(frame, learningRate=learning_rate)

        # Convert grayscale image to RGB color image
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

        # Display the images
        cv2.imshingow('Input', frame)
        cv2.imshow('Output', mask & frame)

        # Checking if the user hit the 'Esc' key
        c = cv2.waitKey(10)
        if c == 27:
            break

    # Releasing the video capture object
    cap.release()
    
    # Closing all the windows
    cv2.destroyAllWindows()