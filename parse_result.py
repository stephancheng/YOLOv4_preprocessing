# -*- coding: utf-8 -*-
"""
Created on Sun May 23 16:12:38 2021

@author: Stephan"""

import re
import pandas as pd

# open file
file = open('test_resultv1.txt')
# class label in the order of class id
classes = ['aquarium','bottle','bowl','box','bucket','plastic_bag','plate','styrofoam','tire','toilet','tub','washing_machine','water_tower']

data = []
count = 0
# loop though each line of the document
for line in file:
    # find every image
    img = re.search('data/test_images/(.*:)', line)
    if img:
        # get image name : XXXX.jpg
        current_img = img.group(0).lstrip('data/test_images/').rstrip(':')
        # record numbers of image
        count += 1
    # for non-image, search if the line contain "left_x", which is an object if yes
    elif re.search('left_x', line):
        # get item name, match xxx_xxx: or xxx:, e.g. plastic_bag: or box:
        item = re.search('[a-z]*_*[a-z]*:', line).group(0).rstrip(':')
        cls_id = classes.index(item) + 1 # get class id from list

        # get the 5 numbers, result is a list ["confidence","x","y","w","h"]
        result = re.findall('\S*[0-9]+', line)
        result[0] = int(result[0])/100 # get confidence in percentage

        new_object =[current_img, cls_id] + result
        data.append(new_object)

column_names = ["image_filename","label_id","confidence","x","y","w","h"]

print("total number of img:", count)
# create dataframe
df = pd.DataFrame(data, columns=column_names)
# reorder the column as required
df = df[["image_filename","label_id","x","y","w","h","confidence"]]
# save result
df.to_csv('summision.csv', index=False)
