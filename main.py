'''
Project name: checkSplitter
File Name : CheckSplitter.py
Authors : Ilay Serr , Gal Erlich, Etai zajonts
Email : ilay92@gmail.com
'''

import plateCrop
import Gui
import cv2
import CheckSplitter

piList = []
piList = Gui.main()
reci = piList[0]
tip = piList[len(piList) - 1]

'''
##### DEFAULT RUN #########
#1. Uncomment this section
#2. Comment all previous section
reci = 'Meal #3/receipt03.png'
tip = 10
piList = [reci, 'Meal #3/breakfast.jpg' ,'Meal #3/pasta.jpg', 10.0]
'''

plates = []
numppl = len(piList) - 2
platePerPerson = []
i = 1

# saves the file then returns filename
def cv2file(img):
    cv2file.counter += 1
    tempString = str(cv2file.counter) + "plate.jpg"
    cv2.imwrite(tempString, img)
    return tempString
cv2file.counter = 0;

while i <= numppl:
    # chack amount of plates in plates
    lastLen = len(plates)
    tempPlates = (plateCrop.findplate(piList[i]))
    for t in tempPlates:
        plates.append(cv2file(t))

    # check the amount of plates added
    lastLen = len(plates) - lastLen
    platePerPerson.append(lastLen)
    i += 1

CheckSplitter.findPrice(reci, platePerPerson, plates, tip)
