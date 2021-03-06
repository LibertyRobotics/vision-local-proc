import numpy as np
import cv2
from networktables import NetworkTables
from grip import GripPipeline

# camera settings
# -1 finds the first camera, so ensure only 1 camera is in
cap = cv2.VideoCapture(2)
cap.set(cv2.CAP_PROP_FPS, 60)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640);
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480);

# pipeline processor object
pipeline = GripPipeline()

# network table initialization
#ip = 6443
#NetworkTables.initialize(ip)
#dashTable = NetworkTables.getTable('SmartDashboard')
#dashTable.putString('vision_test', 6443) # fixxxxxxxx

while (True):
    # Pass in frame from camera (cap)
    ret, frame = cap.read()
    #frame = cv2.imread('powercube.png', 1)

    print('f')
    pipeline.process(frame)

    # set mask and countour frames
    mask = pipeline.mask_0_output
    contour = pipeline.filter_contours_output
    if len(contour) > 0:
        cnt = contour[0]
    # rectangle approximation code (opencv 3.0+ code)
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(frame, [box], 0, (0,0,255), 2)

    # show countour on mask
    cv2.drawContours(mask, contour, -1, (0, 0, 255), 3)

    # show frames mask and default frame
    cv2.imshow('mask', mask)


    cv2.imshow('frame', frame)




    # check if q is hit to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    print("t")
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
