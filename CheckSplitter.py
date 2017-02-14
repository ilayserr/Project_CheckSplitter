'''
Project name: checkSplitter
File Name : CheckSplitter.py
Authors : Ilay Serr , Gal Erlich, Etai zajonts
Email : ilay92@gmail.com
'''

import json
import os
import re
import sys
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
from PIL import Image
from pytesseract import image_to_string



def findPrice(receipt_image_file, user_list, images_names, tip):
    #Clarifai user details
    app = ClarifaiApp("l_ZWZL6TnQ4oj6AabpfJATCDAhID0e-geAo2UWJp", "1bknUExODC3ro13Ehxk6HrgV1PWLJad9FW-01Hd1")
    app.auth.get_token()

    # get the general model
    model = app.models.get("general-v1.3")

    try:
        # get as input the receipt
        receipt = Image.open(receipt_image_file)
    except:
        print ("I'm sorry, something is wrong with the check")
        sys.exit()

    #reads the receipt into a text file
    text = image_to_string(receipt)

    # starting temporary variables
    check = 1;
    count = 0

    # isolating the product lines from the receipt
    pattern = re.findall ('.*[a-zA-Z]+.* \$ [0-9]+.[0-9]+' , text)
    if (len(pattern) == 0):
        print ("I'm sorry, something is wrong with the check")
        sys.exit()

    # initializing the arrays
    patterns_num = []
    patterns_names = []
    patterns_prices = []
    food_images = []
    res_check = []
    res_price = []
    res_name = []
    js = []
    user_list_final = []
    fail_pics = []
    sumCostumer = []
    sum = 0

    for i in range(0 , len(user_list)):
        j = 0
        while (user_list[i] > j):
            user_list_final.append(i + 1)
            j += 1

    # finding the number of product lines
    while ((check != 0) & (count < len(pattern))):
        if (re.findall('SUBTOTAL', pattern[count])):
            check = 0
        else:
            count += 1

    count_new = 0

    # Insert all product nums into an array
    for i in range (0 , count) :
        patterns_num.insert(i ,(int)(re.search('([0-9]+) x' , pattern[i]).group(1)))
        count_new += patterns_num[i]

    pattern_new = []

    for i in range (0, count):
        k = 0
        t = patterns_num[i]
        while (k < t):
            pattern_new.append(pattern[i])
            k += 1

    count = count_new


    patterns_num_new = []
    for i in range (0 , count) :
        patterns_num_new.insert(i ,(int)(re.search('([0-9]+) x' , pattern_new[i]).group(1)))

    try:
        # Insert all product names into an array
        for i in range (0 , count) :
            patterns_names.insert(i ,(re.findall('[0-9]+ x ([a-z]+ [a-z]+|[a-z]+)' , pattern_new[i])[0]))

    except IndexError:
        print ("I'm sorry, something is wrong with the check")
        sys.exit()

    # Insert all product prices into an array
    for i in range (0 , count) :
        patterns_prices.insert( i,(float)(re.findall('\$ ([0-9]+.[0-9]+)' , pattern_new[i])[0]) / patterns_num_new[i])

    # get as input the photos

    while (len(images_names) != count) :
        if (len(images_names) < count) :
            images_names.append('not_found.jpg')
        else :
            i = 0
            while ((i < len(images_names)) and (images_names[i] != 'not_found.jpg')):
                try:
                    os.remove(images_names[i])
                    i += 1
                except:
                    pass

            print ("We found too many plates, sorry")
            sys.exit()

    # inserting the images into an array
    for i in range (0 , count) :
        food_images.insert(i , ClImage(file_obj=open(images_names[i] , 'rb')))


    # insert the model predictions into an array
    for i in range (0 , count) :
        js.insert(i ,model.predict([food_images[i]]))

    for i in range (0, count):
        res_check.insert(i, 0)
        res_price.insert(i , 0)
        res_name.insert(i, 0)
    try:
        # matching each data from the receipt with the suitable image
        for i in range (0 , count) :
            precent = 0
            fail = 0
            for j in range (0 , count):
                if (res_check[j] == 0) :
                    if bool(re.search(patterns_names[i], json.dumps(js[j]))):
                        tempPattern = '"value": 0.[0-9]*, "name": "' + re.escape(patterns_names[i])
                        temp = re.findall(tempPattern, json.dumps(js[j]))[0]
                        valueTemp = float(re.findall('0.[0-9]*', temp)[0])
                        temp = re.findall(tempPattern, json.dumps(js[j]))[0]
                        if (valueTemp > precent):
                            precent = valueTemp
                            res_price[j] = patterns_prices[i]
                            res_name[j] = patterns_names[i]
                            check = j
                            fail = 1
            if (fail == 0):
                fail_pics.append(i)
            else:
                res_check[check] = 1
    except:
        print ("I'm sorry, something is wrong")
        sys.exit()

    pointer = 0

    for i in range (0, count):
        if (res_check[i] == 0) :
            res_price[i] = patterns_prices[fail_pics[pointer]]
            res_name[i] = patterns_names[fail_pics[pointer]]
            if (len(fail_pics) > pointer + 1): pointer += 1

    tip = 1 + (tip / 100.0)

    # deletes the temporary files
    i = 0

    while ((i < len(images_names)) and (images_names[i] != 'not_found.jpg')):
        try:
            os.remove(images_names[i])
            i += 1
        except: pass

    check = 0
    for i in range (0, user_list_final[len(user_list_final) - 1]):
        sumCostumer.insert(i , 0);

    #printing the results
    for i in range (0, count):
        if (res_check[i] != 0):
            print "I know costumer number " , user_list_final[i] , " ordered a " + res_name[i] + \
                                    " and you need to pay " , round((res_price[i] * tip), 2) , "$ with tip included"
            sumCostumer[user_list_final[i] - 1] += round((res_price[i] * tip), 2);
            sum += round((res_price[i] * tip), 2)
            check = 1
    if (check == 1):
        for i in range(0, len(sumCostumer)):
            print "Costumer number", i + 1, "needs to pay a total of ",  sumCostumer[i] , "$ with" \
                                                                                                        " tip included"

        output =  "I didnt recognize the product: "
        for i in range(0, len(fail_pics)):
            if (len(fail_pics) != i + 1):
                output += " " + patterns_names[fail_pics[i]] + ", "
            else:
                output += " " + patterns_names[fail_pics[i]] + ". "
                print output

        print "\nThe total sum that I recognized including the tip is " , sum , "$"
    else:
        print "There is no result to show you, sorry!"