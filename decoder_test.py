'''
This file should decode the information in watermarked pic and return the encoded info.
Author: Will Long
Date: 11/05/2019
'''

import numpy as np
import cv2
import pytesseract
from skimage.measure import compare_ssim
from matplotlib import pyplot as plt

# We need to add tesseract to the right file path. Do later?
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

def get_diff(im1, im2):
    '''
    This function should return the difference between two images as a greyscale image.
    :param im1: String, file path to the first image
    :param im2: String, file path to the second image.
    :return: diff:  the greyscale difference as an image
             score: float [-1,1],   structural similarity index between the two input images. This value can fall into
             the range [-1, 1] with a value of one being a “perfect match”.
    '''

    image1 = cv2.imread(im1)
    image2 = cv2.imread(im2)
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    (score, diff) = compare_ssim(gray1, gray2, full=True)
    diff = (diff * 255).astype("uint8")
    return diff, score

def decode_info(image):
    '''
    This function should return the encoded info in the gray scale image from get_diff.
    :param image: a greyscale image
    :return: code: String, the encoded info
    '''

    txt = pytesseract.image_to_string(image)
    return txt

def decode_watermark(image):
    '''
    This function should decode the info in the watermarked image.
    :param image: String, file path to the watermarked image.
    :return: code: String, the encoded info
    '''
    '''

    diff, score = get_diff(im1, im2)
    code = decode_info(diff)
    '''
    img = cv2.imread(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(img, 250, 255, cv2.THRESH_BINARY_INV)
    code = decode_info(thresh)

    return code

if __name__ == "__main__":

    og_image = r'C:\Users\Will\PycharmProjects\FE_595_Project\Watermark\test.png'
    wm_image = r'C:\Users\Will\PycharmProjects\FE_595_Project\Watermark\test_text.png'
    diff, score = get_diff(og_image, wm_image)
    code = decode_watermark(wm_image)
    print(code)




