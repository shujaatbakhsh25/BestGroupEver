'''
This file should decode the information in watermarked pic and return the encoded info.
Author: Will Long
Date: 11/15/2019
'''

import numpy as np
import cv2
import pywt

def code_ext(OG, W,  L, alp):

    '''
    This should extract a bit stream from the watermarked array.
    :param OG: The Og array
    :param W: The watermarked array
    :param L: Int, the length of the code you want
    :param alp: float on [0,1], the strength of the watermark
    :return: the bit stream
    '''

    '''This part doesn't work. Not sure why. :/'''

    if OG.shape != W.shape: return 'Error: Wrong shapes'
    OG = OG.flatten()
    W = W.flatten()
    #diff = np.absolute(OG - W)
    #diff[diff > 100] = 0 #this gets rid of errors, I hope.
    ind = np.argpartition(OG, -L)[-L:]
    w = []
    for i in ind:
        a = (W[i] - OG[i])/(alp * OG[i])
        w.append(np.sign(a))

    return w

def decode_binary_string(s):
    n = int(s, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(errors='replace')
    #return ''.join(chr(int(s[i*8:i*8+8],2)) for i in range(len(s)//8))


def decode_bit(w):
    '''
    This should decode the bit stream and return the code.
    :param w: 1D Array of {-1,1}, the bit stream
    :return: a string which is the code
    '''

    L = len(w)
    bi_str = '0b'
    for i in range(L):
        if w[i] == 1: bi_str = ''.join([bi_str, '1'])
        if w[i] == -1: bi_str = ''.join([bi_str, '0'])

    #code = bi_str
    code = decode_binary_string(bi_str)

    return code

def decode_watermark(path_OG, path_W, L, alp, method):
    '''
    This function should decode the info in the watermarked image.
    :param path_OG: String, file path to the OG image.
    :param path_W: String, file path to the watermarked image.
    :param L: Int, the length of the code you want
    :param alp: alp: float on [0,1], the strength of the watermark
    :param method: String, method used for the DWT
    :return: the info encoded in the watermark
    '''
    colors_OG = cv2.split(cv2.imread(path_OG))
    colors_W = cv2.split(cv2.imread(path_W))
    codes = []
    for c in range(3):
        OG_c = colors_OG[c]
        OG = pywt.wavedec2(OG_c, method)[-2][2]
        W_c = colors_W[c]
        W = pywt.wavedec2(W_c, method)[-2][2]

        w = code_ext(OG, W,  L, alp)
        code = decode_bit(w)
        codes.append(code)

    code_dic = {
        "Blue Code":codes[0],
        "Green Code":codes[1],
        "Red Code":codes[2]
    }
    return code_dic

if __name__ == "__main__":
    path_OG = r'C:\Users\Will\PycharmProjects\FE_595_Project\Watermark\Test.png'
    path_W = r'C:\Users\Will\PycharmProjects\FE_595_Project\Watermark\Test_W.png'
    seed = "ASDFGHJKLZXCVBNM"
    seed_bin = seed.encode()
    #L = len(seed_bin)-2
    L = 128 # make sure to change that if you change the seed!
    alp = 0.05
    method = 'haar'
    codes = decode_watermark(path_OG, path_W, L, alp, method)


