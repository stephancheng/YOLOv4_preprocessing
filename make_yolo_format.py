# -*- coding: utf-8 -*-
"""
Created on Sat May 22 18:06:49 2021

@author: Stephan
"""

import glob
import os
import pickle
import xml.etree.ElementTree as ET
from os import listdir, getcwd
from os.path import join

# List of class for reference
classes = ['aquarium','bottle','bowl','box','bucket','plastic_bag','plate','styrofoam','tire','toilet','tub','washing_machine','water_tower']

def getImagesInDir(dir_path):
    # Create list with all the imagesname inside
    # dir_path # = ./train_cdc/train_images'
    image_list = []
    for filename in glob.glob(dir_path + '/*.jpg'):
        image_list.append(filename)

    return image_list

def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(dir_path, output_path, image_path):
    basename = os.path.basename(image_path)
    basename_no_ext = os.path.splitext(basename)[0]

    in_file = open(dir_path + '/' + basename_no_ext + '.xml')
    out_file = open(output_path + '/' + basename_no_ext + '.txt', 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    # loop over every labeled object in the xml file
    for obj in root.iter('object'):
        # difficult = obj.find('difficult').text
        cls = obj.find('name').text # get the class label
        if cls not in classes: # or int(difficult)==1:
            print(cls)
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b) # convert into (x,y,w,h)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

cwd = getcwd()
'''
file structure

train_cdc
    train_annotations
    train_images
test_cdc
    test_images

Output file structure
    train_cdc
        train_annotations
        train_images
            XXX.jpg
            xxx.txt
    test_cdc
        test_images
'''

xml_folder = cwd + '/train_cdc/train_annotations'
img_folder = cwd + '/train_cdc/obj'

print('getting image xml from: ',xml_folder)
print('image from: ',img_folder)

image_paths = getImagesInDir(img_folder) # create path to images

for image_path in image_paths:
    convert_annotation(xml_folder, img_folder, image_path)

print("Finished processing: ")
