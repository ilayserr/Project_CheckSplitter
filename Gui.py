'''
Project name: checkSplitter
File Name : CheckSplitter.py
Authors : Ilay Serr , Gal Erlich, Etai zajonts
Email : ilay92@gmail.com
'''

# imports
from tkFileDialog import askopenfilename
from tkinter import Tk, Label, Button, Entry, Message
import cv2
import numpy as np
import urllib



def exit(self):
     #self.master.destroy()
     return params

# read receipt image
def getrec():
    global rec_path
    rec_path = askopenfilename()
    if (rec_path == ''):
        Label(text="0").grid(row=0, column=2)
    else:
        Label(text="1").grid(row=0, column=2)
    return rec_path

# read food images
def getim():
    global i
    images.insert(i, askopenfilename())
    if (images[i]):
        i += 1
    else:
        # in case user enterd the choose window and exited
        del images[-1]
    Label(text=i).grid(row=1, column=2)
    return images

# Gathering information and entering it to params
def callback():
    try:
        final_tip = float(tip.get())
        if (final_tip < 0): final_tip = 0
        params.insert(0, final_tip)
        j = len(images) - 1
        if (j < 0):
            del params[-1]
            t = images[-10]
        while (j >= 0):
            params.insert(0, images[j])
            j -= 1
        if (rec_path == ''):
            t = images[-2]
        params.insert(0, rec_path)
        master.destroy()

    # if one (or more) of the argument was unvalid
    except Exception :
        image = url_to_image("https://s-media-cache-ak0.pinimg.com/564x/30/d1/ae/30d1ae0ab0ffd8df5b325a57128e721b.jpg")
        resized = cv2.resize(image, (500 , 600))
        cv2.imshow("Image", resized)
        cv2.waitKey(3000)
        cv2.destroyAllWindows()



# download the image, convert it to a NumPy array, and then read
# it into OpenCV format
def url_to_image(url):
    resp = urllib.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    # return the image
    return image

# main function
def main():
    global master
    master = Tk()
    master.wm_title("IGI restaurant")

    global tip
    global params
    params = []
    global images
    images = []
    global i
    i = 0

    # labels
    Label(master, text="Choose the receipt image: ").grid(row=0, column=0)
    Label(master, text="0").grid(row=0, column=2)
    Label(master, text="Choose the picture you want to upload:  ").grid(row=1, column=0)
    Label(master, text="0").grid(row=1, column=2)
    Label(master, text="Enter how much tip you want to give:").grid(row=2, column=0)

    # entering the tip input into "tip"
    tip = Entry(master)
    tip.grid(row=2, column=1)

    # calling the getrec function when choosing the suitable "choose" button
    rec_choose = Button(master, text="Choose", command=getrec)
    rec_choose.grid(row=0, column=1)

    # calling the getim function when choosing the suitable "choose" button
    image_choose1 = Button(master, text="Choose", command=getim)
    image_choose1.grid(row=1, column=1)

    # calling the callback function when choosing the suitable "apply" button
    b_apply = Button(master, text="Apply", command=callback)
    b_apply.grid(row=4, column=1)

    master.mainloop()

    # returning final arguments
    return params
