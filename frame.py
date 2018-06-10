import cv2
import numpy as np
import time

cap = cv2.VideoCapture('temp.h264')

while(cap.isOpened()):

    ret, frame = cap.read()
    print(frame.shape)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    time.sleep(0.03)

cap.release()
cv2.destroyAllWindows()
