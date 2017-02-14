'''
Project name: checkSplitter
File Name : CheckSplitter.py
Authors : Ilay Serr , Gal Erlich, Etai zajonts
Email : ilay92@gmail.com
'''


import numpy as np
import cv2

# main find plate function
def findplate(imagepath):
    # read Image 2 cv2 obj
    image = cv2.imread(imagepath)
    # turn gray
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # blur - improve false positive
    gray2 = cv2.GaussianBlur(gray, (5,5), 0)

    # detect circles in the image
    circles = cv2.HoughCircles(gray2, cv2.cv.CV_HOUGH_GRADIENT, 2, 300, 400, 600, 150)  #200 , 300

    # ensure at least some circles were found
    if circles is not None:

        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")

        # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:

            # draw the circle in the output image, then draw a rectangle
            # corresponding to the center of the circle
            cv2.circle(gray2, (x, y), r, (255, 255, 255), 4)
            cv2.rectangle(gray2, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

    plates = []
    # crop plates and glasses
    if circles is not None:
        # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            h, w = gray.shape[0:2]
            ymin = max(y - r - 5, 0)
            ymax = min (y + r + 5, h)
            xmin = max(x - r - 5, 0)
            xmax = min(x + r + 5, w)
            plates.append((image[ymin:ymax, xmin:xmax]))

    '''
    ##### To show the crop and circles calculations ######
    #1. Uncomment this section of code

    # show the output image
    cv2.imshow("output", np.hstack([gray, gray2]))
    cv2.waitKey(0)

    # show the crop images
    for i in plates:
        cv2.imshow("crop", i)
        cv2.waitKey(0)
    '''

    return plates
