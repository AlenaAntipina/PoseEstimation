import os
import sys
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

width = 1280
height = 720
folderPath = "test"
filename = 'result.png'
gestureThreshold = 300
height_small = int(144*1)
width_small = int(256*1)
imgNumber = 0

# Camera Setup
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

detectorHand = HandDetector(detectionCon=0.8, maxHands=1)

# Get whiteboard for drawn
pathImage = os.listdir(folderPath)

annotations = [[]]
annotationNumber = -1
annotationStart = False

while True:
    success, img = cap.read()   # import image
    img = cv2.flip(img, 1)
    path = os.path.join(folderPath, pathImage[0])
    imgCurrent = cv2.imread(path)
    hands, img = detectorHand.findHands(img, flipType=False)

    if hands:
        hand = hands[0]
        fingers = detectorHand.fingersUp(hand)
        center_x, center_y = hand['center']
        lmList = hand["lmList"]  # List of 21 Landmark points
        xVal = int(np.interp(lmList[8][0], [width // 3, width], [0, width]))
        yVal = int(np.interp(lmList[8][1], [150, height - 150], [0, height]))
        indexFinger = xVal, yVal

        if center_y <= gestureThreshold:      # if hand at the height of the head
            # gesture 1 - close (use rock at the height of the head)
            if fingers == [1, 0, 0, 0, 0]:
                cv2.imwrite(filename, cur_image)
                print("close")
                sys.exit()

        # gesture 2 - show pointer (use 2 fingers)
        if fingers == [1, 1, 1, 0, 0]:
            cv2.circle(imgCurrent, indexFinger, 10, (255, 0, 0), cv2.FILLED)
            annotationStart = False

        # gesture 3 - draw (use 1 finger)
        if fingers == [1, 1, 0, 0, 0]:
            if annotationStart is False:
                annotationStart = True
                annotationNumber += 1
                annotations.append([])
            cv2.circle(imgCurrent, indexFinger, 10, (255, 0, 0), cv2.FILLED)
            annotations[annotationNumber].append(indexFinger)
        else:
            annotationStart = False

    for i in range(len(annotations)):
        for j in range(len(annotations[i])):
            if j != 0:
                cur_image = cv2.line(imgCurrent, annotations[i][j-1], annotations[i][j], (255, 0, 0), 10)

    # Add webcam image on the slide
    imgSmall = cv2.resize(img, (width_small, height_small))
    h, w, _ = imgCurrent.shape
    imgCurrent[0:height_small, w-width_small:w] = imgSmall

    # cv2.imshow("Image", img)
    cv2.imshow("Whiteboard", imgCurrent)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

