import os
import numpy as np
import pytesseract
import cv2
from os import path
from os import listdir
from os.path import isfile, join
from prune_and_extract_text import extract_text, match

def comp(val): 
	val = val[:-4]
	return int(val) 

mypath = '/home/kmba/Documents/Python/ANPR/Test_data/'
files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
files.sort(key = comp)
print(files)
batch = []
for input_image in files:
    os.system("python detect.py --source Test_data/" + input_image + " --weights weights/last.pt --save-txt")
    cropped_image = input_image[:-4] + '_cropped.jpg'
    cropped_image_path = 'inference/output/' + cropped_image
    if path.exists(cropped_image_path) == False:
    	continue

    #print(cropped_image_path)
    #print()
    img = cv2.imread(cropped_image_path)
    img = cv2.resize(img, None, fx=1.6, fy=1.6, interpolation=cv2.INTER_CUBIC)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((2, 2), np.uint8)
    # 2 is better than 1
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)
    #bilateral is better than median
    img = cv2.threshold(cv2.bilateralFilter(img, 5, 75, 75), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


    cv2.imwrite(cropped_image_path, img)
    #data = pytesseract.image_to_string(thresh, lang='eng', config='--psm 6')
    #print(data)
    output = extract_text(cropped_image_path, 'out')
    batch.append(output)
    f=open('Analysis/model_res1.txt','a+')
    f.write(output)
    f.close()

print(batch)