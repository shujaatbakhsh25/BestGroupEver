'''
This file should add a barium pill, i.e. a watermark, that we can use to trace the follow of a picture.
Author: Will Long
Date: 11/27/2019
'''

import numpy as np
import cv2
import pywt
import reedsolo as reed
import qrcode


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
    '''
    for i in range(L):
        if w[i] == 1 and A[i] < A[i+1]:
            A[i+1], A[i] = A[i], A[i+1]
        elif w[i] == -1 and A[i] > A[i+1]:
            A[i + 1], A[i] = A[i], A[i + 1]
    '''

    A = np.reshape(A, shape)
    return A

def encode_QR(string):
    '''
    This fun should take a string, encode it in a QR code, flatten the QR code into a 1D Array, and return that array.
    :param string: String
    :return: 1D array of {0,1}
    '''
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=1,
        border=0,
    )
    qr.add_data(string)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img_array = np.array(img)
    img_bin = img_array.astype(int)
    img_flat = img_bin.flatten()
    return img_flat

def con_to_bit(string):
    '''
    this should convert a string into a binary array of {-1,1}
    :param string: String
    :return: binary array of {-1,1}
    '''
    '''
    rs = reed.RSCodec(100)  # This should help with errors. I think.

    res = bin(int.from_bytes(rs.encode(string.encode()), 'big'))
    '''
    res = encode_QR(string).astype(str)
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
        np_coeffs = [np.asarray(x) for x in coeffs]
        for j in range(len(coeffs[-2])):
            B = coeffs[-2][j]
            Bp = code_embed(B, w, alp)
            np_coeffs[-2][j] = Bp

        Aw = image_rec(np_coeffs, method)
        colors_w.append(Aw)

    img_w = cv2.merge(colors_w)
    return img_w


if __name__ == "__main__":
    image_path = r'C:\Users\doom6\Documents\Python projects\FE_595_Project\Watermark\Test.png'
    seed = """ASDFGHJ"""
    alp = 0.5
    method = 'haar'
    image_watermark = add_watermark(image_path, seed, alp, method)
    cv2.imwrite(r'C:\Users\doom6\Documents\Python projects\FE_595_Project\Watermark\Test_W.png', image_watermark)