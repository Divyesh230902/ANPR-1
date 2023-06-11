from django.shortcuts import render
import cv2
import numpy as np
import matplotlib.pyplot as plt
import easyocr
from io import BytesIO
from django.core.files.base import ContentFile
import matplotlib
matplotlib.use("agg")
from .models import image_storage

# Create your views here.

def detect_plate(path): #making a function
    # img=cv2.imread(path) #reading the path
    img = cv2.imdecode(np.fromstring(path.read(),np.uint8),cv2.IMREAD_UNCHANGED)
    img = cv2.resize(img, (250, 250)) #resizing the image
    image_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #convert to grayscale
    image_blur = cv2.GaussianBlur(image_gray, (5, 5), 0) #blur the grayscale image
    image_canny = cv2.Canny(image_blur, 150, 200) #edge detection
    contours, hierarchy = cv2.findContours(image_canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #Find all the contours in the image
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    for c in contours:
        perimeter = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02*perimeter, True)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            break
    mask = np.zeros(image_gray.shape, np.uint8)
    new_image = cv2.drawContours(mask, [approx], 0, 255, -1)
    new_image = cv2.bitwise_and(img, img, mask=mask)
    (x, y) = np.where(mask == 255)
    (topx, topy) = (np.min(x), np.min(y))
    (bottomx, bottomy) = (np.max(x), np.max(y))
    Cropped = img[topx:bottomx+1, topy:bottomy+1]
    plt.figure(figsize=(20,10))
    plt.subplots_adjust(wspace=0, hspace=0)
    plt.subplot(1,3,2),plt.imshow(cv2.cvtColor(new_image,cv2.COLOR_BGR2RGB))
    plt.subplot(1,3,1),plt.imshow(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
    plt.subplot(1,3,3),plt.imshow(cv2.cvtColor(Cropped,cv2.COLOR_BGR2RGB))
    final_img = BytesIO()
    plt.savefig(final_img, bbox_inches="tight", pad_inches=0,)
    ocr = easyocr.Reader(['en'])
    ocr = ocr.readtext(Cropped)
    return ocr,final_img


def get_form(request):
    return render(request,'addimage.html')

def get_data(request):
    if request.method == "POST":

        image = request.FILES["image"]
        ocr,final_img = detect_plate(image)
        ocr_output = ""
        for output_ocr in ocr:
            ocr_output += output_ocr[-2] + " "
        print(ocr)
        final_img = ContentFile(final_img.getvalue())
        db_object = image_storage.objects.create(ocr_output=ocr_output)
        db_object.img.save(image.name,final_img)
        db_object.save()
        return render(request,'show_output.html',context={"image":db_object})

