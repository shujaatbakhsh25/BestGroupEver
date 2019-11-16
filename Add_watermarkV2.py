'''
This file should add a barium pill, i.e. a watermark, that we can use to trace the follow of a picture.
Author: Will Long
Date: 11/15/2019
'''

import numpy as np
import cv2
import pywt

def image_rec(coeffs, method):
    '''
    This should reconstruct an image from the DWT coeffs in a usable way
    :param coeffs: NP array, DWT coeffs
    :param method: String, method used for the reconstruction
    :return: NP array for the image
    '''
    img = pywt.waverec2(coeffs, method)
    img = img.astype(int)
    #img = img[:, :, :3]
    return img

def code_embed(A, w, alp):
    '''
    This should embed a bit stream into the array A.
    :param A: Array, the cover array
    :param w: List of {-1,1}, the bit stream
    :param alp: float on [0,1], the strength of the watermark
    :return: the watermarked array
    '''

    shape = A.shape
    A = A.flatten()
    L = len(w)
    A_cut = A
    #A_cut[A>200] = 0 # maybe I should cut off really big values?
    ind = np.argpartition(A_cut, -L)[-L:]
    k = 0
    for i in ind:
        a = A[i] + alp * A[i] * w[k]
        A[i] = a
        k += 1

    A = np.reshape(A, shape)
    return A

def con_to_bit(string):
    '''
    this should convert a string into a binary array of {-1,1}
    :param string: String
    :return: binary array of {-1,1}
    '''

    #res = ''.join(format(i, 'b') for i in bytearray(string, encoding='utf-8'))
    #res = str(res)
    res = bin(int.from_bytes(string.encode(), 'big'))
    a = []
    for i in range(len(res)):
        if res[i] == '1': a.append(1)
        if res[i] == '0': a.append(-1)

    return np.array(a)

def add_watermark(path, seed, alp, method):
    '''
    This function should add a watermark to the picture using DWT.
    :param path: String, the file path of the picture
    :param seed:  String, the code used to generate the watermark
    :param alp: float on [0,1], the strength of the watermark
    :param method: String, method used for the DWT
    :return: Array, the watermarked image
    '''

    img = cv2.imread(path)
    colors = cv2.split(img) # You have to split the colors, otherwise DWT doesn't work.
    colors_w = []
    w = con_to_bit(seed)
    for c in range(3):
        A = colors[c]
        coeffs = pywt.wavedec2(A, method)
        B = coeffs[-2][2]
        Bp = code_embed(B, w, alp)
        np_coeffs = [np.asarray(x) for x in coeffs]
        np_coeffs[-2][2] = Bp
        Aw = image_rec(np_coeffs, method)
        colors_w.append(Aw)

    img_w = cv2.merge(colors_w)
    return img_w














if __name__ == "__main__":
    image_path = r'C:\Users\Will\PycharmProjects\FE_595_Project\Watermark\Test.png'
    seed = "ASDFGHJKLZXCVBNM"
    alp = 0.05
    method = 'haar'
    image_watermark = add_watermark(image_path, seed, alp, method)
    cv2.imwrite(r'C:\Users\Will\PycharmProjects\FE_595_Project\Watermark\Test_W.png', image_watermark)