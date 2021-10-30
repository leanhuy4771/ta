from flask import Flask, Response,request, render_template
import logging
import lxml.html
import urllib.request as urllib2
import pprint
import http.cookiejar as cookielib
from io import BytesIO
import lxml.html
from PIL import Image, ImageFilter, ImageOps, ImageChops
import pytesseract
import requests
import cv2
import urllib
app = Flask(__name__)
 
@app.route('/')  
def upload():  
    return render_template("file_upload_form.html")  
 
@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']  
        f.save(f.filename)
        img = cv2.imread(f.filename)
        gry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        (h, w) = gry.shape[:2]
        gry = cv2.resize(gry, (w*2, h*2))
        cls = cv2.morphologyEx(gry, cv2.MORPH_CLOSE, None)
        thr = cv2.threshold(cls, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        txt = pytesseract.image_to_string(thr) 
        return render_template("success.html", name = txt)  
  
if __name__ == '__main__':  
    app.run(debug = True)  