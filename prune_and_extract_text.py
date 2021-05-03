import os
import sys

def run_tesseract(img_path, filename):
    os.system("python ocr.py " + img_path + " > " + filename)

def preprocess_text(line):
    stop_words = ["[","]","{","}",".","|",","," ","-","_","(",")","\\",":","\"","=","!","—",";","'","‘","“","°","/","$","<",">","+"]
    res = ''
    for word in line:
        if word not in stop_words:
            res += word.upper()
    return res

def extract_text(img_path, filename):
    run_tesseract(img_path, filename)
    f = open(filename).readlines()
    f.reverse()
    line = ""
    for line in f:
        line = preprocess_text(line)
        if len(line) >= 8  and "HOND" not in line:
            break
    return line

def match(num):
    stop_plate = [0,"","0"]
    suspected = ''
    from similarity.cosine import Cosine
    cosine = Cosine(2)
    s0 = str(num)
    f = open('lic.csv').readlines()
    for s1 in f:
        s1 = s1.replace("\n", "")
        if s1 in stop_plate:
            continue
        print(s1)
        p0 = cosine.get_profile(s0)
        p1 = cosine.get_profile(s1)
        if cosine.similarity_profiles(p0, p1) >= 0.65:
            suspected += s1 + " "
    return suspected
