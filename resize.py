from PIL import Image  
import os
from os import listdir
from os.path import isfile, join

mypath = '/home/kmba/Documents/Python/ANPR/Test_data_ishaan/'
files = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for input_image in files:
	im = Image.open(mypath + input_image)
	im=im.rotate(270, expand=True)
	newsize = (960, 1280) 
	im1 = im.resize(newsize)
	im1 = im1.save(mypath + input_image)

