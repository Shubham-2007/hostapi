# from django.shortcuts import render

# Create your views here.
# from django.shortcuts import render
# from django.http import JsonResponse
# from rest_framework.decorators import api_view
# from django.shortcuts import render
# from django.http import JsonResponse
# from django.conf import settings
# from .apps import FileAppConfig
# from rest_framework.decorators import api_view
# from PIL import ImageGrab, Image
# import numpy as np
# from PIL import ImageDraw
# import cv2
# import os
# import time
# import glob
# import requests
# import json
# import io
# heroku git:remote -a apiprohost set git remote heroku to https://git.heroku.com/apiprohost.git

from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from .apps import ApiConfig
from rest_framework.decorators import api_view
from PIL import ImageGrab, Image
import numpy as np
from PIL import ImageDraw
import cv2
import os
import time
import glob
import requests
import json
import io
from PIL import Image
from numpy import asarray 
from rest_framework.views import APIView
# from rest_framework.parsers import MultiPartParser, FormParser
# from rest_framework.response import Response
# from rest_framework import status
 
class getimagefromrequest(APIView):
    # parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        image = request.data
        print("image:", image) 
        # print("image00:", asarray(Image.open(image['file'])))
        # image_bytes = image['file'].read()
        # print("image1:", image_bytes) 
        print(Image.open(image['file'])) 
        img = asarray(Image.open(image['file']))
        print(img)     
        #Read image data from the network and convert it into image format:
        # img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), -1)
        # print("image2:", np.frombuffer(image_bytes, np.uint8)) 
        
        
        # print("image2:", img) 
        # img2 = np.array(image['file'])
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
    # apply otsu thresholding
        ret, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV, cv2.THRESH_OTSU)
    # find the contours
        contours = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        for cnt in contours:
        # get bounding box and exact region of interest
            x, y, w, h = cv2.boundingRect(cnt)
        # create rectangle
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 1)
            top = int(0.05 * th.shape[0])
            bottom = top
            left = int(0.05 * th.shape[1])
            right = left
            th_up = cv2.copyMakeBorder(th, top, bottom, left, right, cv2.BORDER_REPLICATE)
            # Extract the image's region of interest
            roi = th[y - top : y + h + bottom, x - left : x + w + right]
            #digit, acc = predict_digit(roi)

        img = cv2.resize(roi, (28, 28), interpolation=cv2.INTER_AREA)
    # cv2.imshow("img", img)
        img = img.reshape(1, 28, 28, 1)
    # normalizing the image to support our model input
        img = img / 255.0
    #   img=img.convert('L')
    #   img=np.array(img)
    #   print(img)
    # reshaping to support our model and normalizing
    #   img=img.reshape(1,28,28,1)
    #   img=img/255.0
    #   print(img.size)
    #   temp=np.array(img)
    #   flat=temp.ravel()
    #   print(flat.size)
    # predicting the class
        res = ApiConfig.digitmodel.predict([img])[0]

        return JsonResponse({"digit": str(np.argmax(res)), "acc": str(max(res))})
 

# from keras.models import load_model
# from tkinter import *
# import tkinter as tk
# from PIL import ImageGrab, Image
# import numpy as np
# from PIL import ImageDraw
# import cv2

# model = load_model("digitdemo1.h5")


# def predict_digit(img):
#     # resize image to 28x28 pixels
#     #   img=img.resize((28,28))
#     img = cv2.resize(img, (28, 28), interpolation=cv2.INTER_AREA)
#     print(img.size)
#     # convert rgb to grayscale
#     cv2.imshow('img', img)
#     img = img.reshape(1, 28, 28, 1)
#     # normalizing the image to support our model input
#     img = img / 255.0
#     #   img=img.convert('L')
#     #   img=np.array(img)
#     #   print(img)
#     # reshaping to support our model and normalizing
#     #   img=img.reshape(1,28,28,1)
#     #   img=img/255.0
#     #   print(img.size)
#     #   temp=np.array(img)
#     #   flat=temp.ravel()
#     #   print(flat.size)
#     # predicting the class
#     res = model.predict([img])[0]
#     print("\nIndices of Max element : ", np.argmax(res))
#     print("\nIndices of Max element : ", max(res))
#     print("\nIndices of Max element : ", res)
#     return np.argmax(res), max(res)


# class App(tk.Tk):
#     def __init__(self):
#         tk.Tk.__init__(self)
#         self.x = self.y = 0
#         self.image1 = Image.new("RGB", (500, 500), 'white')  # Image.new(mode, size, color), size=(width,height)
#         self.draw = ImageDraw.Draw(self.image1)
#         # creating elements
#         self.Canvas = tk.Canvas(self, width=500, height=500, bg="white", cursor="cross")
#         self.label = tk.Label(self, text="Thinking..", font=("Helvetica", 48))
#         self.classify_btn = tk.Button(self, text="recognise", command=self.classify_handwriting)
#         self.button_clear = tk.Button(self, text="Clear", command=self.clear_all)

#         # Grid Structure
#         self.Canvas.grid(row=0, column=0, pady=2)
#         self.label.grid(row=0, column=1, pady=2, padx=2)
#         self.button_clear.grid(row=1, column=0, pady=2, padx=2)
#         self.classify_btn.grid(row=1, column=1, pady=2)

#         # self.Canvas.bind("<Motion>",self.start_pos)
#         self.Canvas.bind("<B1-Motion>", self.draw_lines)

#     def clear_all(self):
#         self.Canvas.delete("all")
#         self.draw.rectangle((0, 0, 500, 500), fill='white')

#     def classify_handwriting(self):
#         #         x=self.tk.winfo_rootx()+self.Canvas.winfo_x()
#         #         y=self.tk.winfo_rooty()+self.Canvas.winfo_y()
#         #         x1=x+self.Canvas.winfo_width()
#         #         y1=y+self.Canvas.winfo_height()
#         #         im=ImageGrab.grab().crop((x,y,x1,y1))
#         #         HWND=self.Canvas.winfo_id()#to get the handle of the Canvas
#         #         rec=win32gui.GetWindowRect(HWND)#get the coordinates of the Canvas
#         #         a,b,c,d = rec
#         #         print(a,b,c,d)
#         #         rec=(a,b,c,d)
#         #         im=ImageGrab.grab(rec)
#         #         self.image1.show()
#         # print("image1",image1)
#         print("image2",self.image1) 
#         img = np.array(self.image1)
#         print(img) 
#         # convert the image into grayscale
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         # apply otsu thresholding
#         ret, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV, cv2.THRESH_OTSU)
#         # find the contours
#         contours = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
#         for cnt in contours: 
#             # get bounding box and exact region of interest
#             x, y, w, h = cv2.boundingRect(cnt)
#             # create rectangle
#             cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 1)
#             # cv2.rectangle(image, start_point, end_point, color, thickness)
#             # image: It is the image on which rectangle is to be drawn.
#             # start_point: It is the starting coordinates of rectangle. The coordinates are represented as tuples of two values i.e. (X coordinate value, Y coordinate value).
#             # end_point: It is the ending coordinates of rectangle. The coordinates are represented as tuples of two values i.e. (X coordinate value, Y coordinate value).
#             # color: It is the color of border line of rectangle to be drawn. For BGR, we pass a tuple. eg: (255, 0, 0) for blue color.
#             # thickness: It is the thickness of the rectangle border line in px. Thickness of -1 px will fill the rectangle shape by the specified color.

#             top = int(0.05 * th.shape[0])
#             bottom = top
#             left = int(0.05 * th.shape[1])
#             right = left

#             th_up = cv2.copyMakeBorder(th, top, bottom, left, right, cv2.BORDER_REPLICATE)
#             # Extract the image's region of interest

#             roi = th[y - top:y + h + bottom, x - left:x + w + right]
#             digit, acc = predict_digit(roi)
#             self.label.configure(text=str(digit) + ', ' + str(int(acc * 100)) + '%')
#             cv2.destroyAllWindows()

#     def draw_lines(self, event):
#         self.x = event.x
#         self.y = event.y
#         r = 20
#         self.Canvas.create_oval(self.x - r, self.y - r, self.x + r, self.y + r, fill='black')
#         self.draw.ellipse([(self.x - r, self.y - r), (self.x + r, self.y + r)], fill='black')


# app = App()
# mainloop()







































# # Create your views here.
# @api_view(['POST'])  # recieve the request
# def getimagefromrequest(request):
#     # if request.method == 'POST':
#     # print('POST',request.data.get('image'))
#     # body = json.loads(request.body)
#     image = request.FILES.get("image")
#     print("image:", type(image.file))
#     image_bytes = image.read()
#     #print(image_bytes)
#     # final_image = np
#     print('hello')
#     #digit, acc = classify_handwriting(image_bytes)
#     #print(str(digit))

# # print('image type:',type(image))
#     # img = np.array(image)
#     img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), -1)
#     # print('decoded', img)
#     print(img.shape)
#     # converting to grayscale
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     # apply otsu thresholding
#     ret, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV, cv2.THRESH_OTSU)
#     # find the contours
#     contours = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
#     for cnt in contours:
#         # get bounding box and exact region of interest
#         x, y, w, h = cv2.boundingRect(cnt)
#         # create rectangle
#         cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 1)
#         top = int(0.05 * th.shape[0])
#         bottom = top
#         left = int(0.05 * th.shape[1])
#         right = left
#         th_up = cv2.copyMakeBorder(th, top, bottom, left, right, cv2.BORDER_REPLICATE)
#         # Extract the image's region of interest
#         roi = th[y - top : y + h + bottom, x - left : x + w + right]
#         #digit, acc = predict_digit(roi)

#     img = cv2.resize(roi, (28, 28), interpolation=cv2.INTER_AREA)
#     # cv2.imshow("img", img)
#     img = img.reshape(1, 28, 28, 1)
#     # normalizing the image to support our model input
#     img = img / 255.0
#     #   img=img.convert('L') 
#     #   img=np.array(img)
#     #   print(img)
#     # reshaping to support our model and normalizing
#     #   img=img.reshape(1,28,28,1)
#     #   img=img/255.0
#     #   print(img.size)
#     #   temp=np.array(img)
#     #   flat=temp.ravel()
#     #   print(flat.size)
#     # predicting the class
#     res = FileAppConfig.digitmodel.predict([img])[0]








#     return JsonResponse({"digit": str(np.argmax(res)), "acc": str(max(res))})
 