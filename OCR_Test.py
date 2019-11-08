from PIL import Image
import pytesseract
import cv2 as cv
from matplotlib import pyplot as plt


pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'


test = cv.imread('OG.png', cv.COLOR_BGR2GRAY)


txt = pytesseract.image_to_string(test)


txt


ret, bi_img = cv.threshold(test, 250, 255, cv.THRESH_BINARY_INV)


plt.figure(1)
plt.imshow(bi_img, 'gray')
plt.show


txt = pytesseract.image_to_string(bi_img)
