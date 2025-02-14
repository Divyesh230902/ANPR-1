from django.shortcuts import render
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import pytesseract
from io import BytesIO
from django.core.files.base import ContentFile
import matplotlib
matplotlib.use("agg")
from .models import image_storage
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializer import image_serializer

# Create your views here.

def get_plate(img):
    # Convert to grayscale
    img = cv.imread(img)
    img = cv.resize(img, (300, 200))
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # Blur the image
    blur = cv.GaussianBlur(gray, (5, 5), 0)
    # Apply Canny edge detection
    canny = cv.Canny(blur, 150, 200)
    # Find contours
    contours, hierarchy = cv.findContours(canny, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    # Find the contour with the maximum area
    cnt = max(contours, key=cv.contourArea)
    # Find the perimeter of the contour
    perimeter = cv.arcLength(cnt, True)
    # Approximate the contour
    approx = cv.approxPolyDP(cnt, 0.02 * perimeter, True)
    # Draw the contour
    cv.drawContours(img, [approx], -1, (0, 255, 0), 3)
    # Get the coordinates of the contour
    x, y, w, h = cv.boundingRect(approx)
    # Crop the image
    plate = img[y:y+h, x:x+w]
    text = pytesseract.image_to_string(img, lang='eng', config='--psm 6')
    return text, plate


def get_form(request):
    return render(request,'addimage.html')

@api_view(['POST'])
def get_data(request):
    if request.method == "POST":
        print("hello post")
        image = request.FILES["image"]
        db_object = image_storage.objects.create(img_input=image)
        db_object.save()
        print(db_object.img_input.path)
        ocr,final_img = get_plate(db_object.img_input.path)
        print(ocr)
        f_img = cv.imencode('.jpg', final_img)
        final_img = ContentFile(f_img[1].tobytes())
        
        db_object.img.save(image.name,final_img)
        db_object.save()
        ob = image_serializer(db_object)
        return Response(ob.data)

