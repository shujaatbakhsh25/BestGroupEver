'''
This file should decode the information in watermarked pic and return the encoded info.
Author: Will Long
Date: 11/27/2019
'''

import numpy as np
import cv2
import pywt
import reedsolo as reed
import pyzbar.pyzbar as pyzbar
import qrcode

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
    '''
    for i in range(L):
        if W[i] > W[i+1] : w.append(1)
        else: w.append(-1)
    '''


    return w

def w_avg(data):
    '''
    This fun should take an array of bit streams, and then return the average bit stream.
    :param data: 2D Array of {-1,1}
    :return: the average bit stream
    '''

    '''
    n = len(data)
    L = len(data[0])
    w_data = []
    for k in range(n):
        w_row = []
        w_raw = data[k]
        for i in range(L):
            if w_raw[i] == 1: w_row.append(1)
            if w_raw[i] == -1: w_row.append(0)
            else: w_row.append(1)
        w_data.append(w_row)
    w_np = np.array(w_data)
    w_a = []
    for i in range(L):
        a = sum(w_np[:,i])/n
        w_a.append(round(a))
    w_b = []
    for i in range(L):
        if w_a[i] == 1: w_b.append(1)
        if w_a[i] == 0: w_b.append(-1)
    '''
    #data_s = data[0] + data[1] + data[2]
    data_s = data[0]
    for i in range(1, len(data)):
        data_s = data_s + data[i]

    w_b = []
    for i in range(len(data_s)):
        if data_s[i] > 0: w_b.append(1)
        else: w_b.append(-1)

    return np.array(w_b)

def blank_QR():
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=1,
        border=4,
    )
    qr.add_data('')
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img_array = np.array(img)
    img_bin = img_array.astype(int)
    img_bin = np.uint8(img_bin)
    return img_bin
def make_QR(string):
    '''
    This should take a binary string and turn it into a QR code.
    :param string: binary string
    :return: 2D array, a QR code
    '''
    bi = np.uint8(string)
    im_raw = bi.reshape(21, 21)
    im_bin = cv2.copyMakeBorder(im_raw, 4, 4, 4, 4, cv2.BORDER_CONSTANT, value=1)
    im_blank = blank_QR()  # I can fix the parts I know are wrong
    sq = im_blank[3:12, 3:12]
    im_bin[3:12, 3:12] = sq
    im_bin[3:12, 17:26] = sq
    im_bin[17:26, 3:12] = sq
    im_bin[12:17, 10] = [0, 1, 0, 1, 0]
    im_bin[10, 12:17] = [0, 1, 0, 1, 0]
    im_bin = im_bin * 255
    k = 0
    while k < 5:
        height, width = im_bin.shape[:2]
        im_big = cv2.resize(im_bin, (2 * width, 2 * height), interpolation=cv2.INTER_LINEAR)
        ret, im_fin = cv2.threshold(im_big, 127, 255, cv2.THRESH_BINARY)
        im_bin = im_fin
        k +=1



    return im_fin


def decode_QR(string):
    '''
    This should take a binary string, turn it into a QR code, and then decode said QR code
    :param string: binary string
    :return: the encoded info
    '''

    '''
    bi = np.uint8(string)
    im_raw = bi.reshape(21,21)
    im_bin = cv2.copyMakeBorder(im_raw, 4, 4, 4, 4, cv2.BORDER_CONSTANT, value=1)
    im_blank = blank_QR() # I can fix the parts I know are wrong
    sq = im_blank[3:12, 3:12]
    im_bin[3:12, 3:12] = sq
    im_bin[3:12, 17:26] = sq
    im_bin[17:26, 3:12] = sq
    im_bin[12:17, 10] = [0, 1, 0, 1, 0]
    im_bin[10, 12:17] = [0, 1, 0, 1, 0]
    im_bin = im_bin * 255
    height, width = im_bin.shape[:2]
    im_big = cv2.resize(im_bin, (4 * width, 4 * height), interpolation=cv2.INTER_LINEAR)
    ret, im_fin = cv2.threshold(im_big, 127, 255, cv2.THRESH_BINARY)
    '''
    im_fin = make_QR(string)
    decoded = pyzbar.decode(im_fin)
    if len(decoded) == 0: ans = 0
    else: ans = decoded[0].data
    return ans





def decode_binary_string(s):
    n = int(s, 2)

    rs = reed.RSCodec(100)  # This should help with errors. I think.
    byt = n.to_bytes((n.bit_length() + 7) // 8, 'big')
    return rs.decode(byt)
    #return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(errors='replace')
    #return ''.join(chr(int(s[i*8:i*8+8],2)) for i in range(len(s)//8))



def decode_bit(w):
    '''
    This should decode the bit stream and return the code.
    :param w: 1D Array of {-1,1}, the bit stream
    :return: a string which is the code
    '''

    L = len(w)
    '''
    bi_str = '0b'
    for i in range(L):
        if w[i] == 1: bi_str = ''.join([bi_str, '1'])
        if w[i] == -1: bi_str = ''.join([bi_str, '0'])
        else:  ''.join([bi_str, '1'])
    '''
    bi_str = []
    for i in range(L):
        if w[i] == 1: bi_str.append('1')
        if w[i] == -1: bi_str.append('0')


    #code = bi_str
    #code = decode_binary_string(bi_str)
    code = decode_QR(bi_str)

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
    bits = []
    for c in range(3):
        OG_c = colors_OG[c]
        W_c = colors_W[c]
        OG_coeffs = pywt.wavedec2(OG_c, method)
        W_coeffs = pywt.wavedec2(W_c, method)
        color_bits = []
        for j in range(len(OG_coeffs[-2])):
            OG = OG_coeffs[-2][j]
            W = W_coeffs[-2][j]
            wj = code_ext(OG, W, L, alp)
            color_bits.append(wj)
        w = w_avg(np.array(color_bits))
        bits.append(w)
    bits = np.array(bits)
    '''

    for c in range(3):
        w = bits[c]
        code = decode_bit(w)
        codes.append(code)
    '''

    codes = [0,0,0]

    w_a = w_avg(bits)
    avg_code = decode_bit(w_a)
    #avg_code = 0
    code_dic = {
        "Average Code": avg_code,
        "Blue Code": codes[0],
        "Green Code": codes[1],
        "Red Code": codes[2]
    }
    return code_dic, bits


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

def decode_test(path_OG, path_W, L, alp, method, seed):
    '''
    this should show the error in the watermarked info.
    :param path_OG: String, file path to the OG image.
    :param path_W: String, file path to the watermarked image.
    :param L: Int, the length of the code you want
    :param alp: alp: float on [0,1], the strength of the watermark
    :param method: String, method used for the DWT
    :param seed: String, the code used to generate the OG watermark
    :return:
    '''
    w_og = con_to_bit(seed)
    colors_OG = cv2.split(cv2.imread(path_OG))
    colors_W = cv2.split(cv2.imread(path_W))
    codes = []
    bits = []
    for c in range(3):
        OG_c = colors_OG[c]
        W_c = colors_W[c]
        OG_coeffs = pywt.wavedec2(OG_c, method)
        W_coeffs = pywt.wavedec2(W_c, method)
        color_bits = []
        for j in range(len(OG_coeffs[-2])):
            OG = OG_coeffs[-2][j]
            W = W_coeffs[-2][j]
            wj = code_ext(OG, W, L, alp)
            color_bits.append(wj)
        w = w_avg(np.array(color_bits))
        bits.append(w)
    bits = np.array(bits)

    w_edit = w_avg(bits)
    diff = np.absolute(w_og - w_edit)
    error = sum(diff) / (2 * len(diff))

    return error, w_og, w_edit



if __name__ == "__main__":
    path_OG = r'C:\Users\doom6\Documents\Python projects\FE_595_Project\Watermark\Test.png'
    path_W = r'C:\Users\doom6\Documents\Python projects\FE_595_Project\Watermark\Test_W.png'
    seed = """ASDFGHJ"""
    seed_bin = seed.encode()
    #L = len(seed_bin)-2
    #L = 128 # make sure to change that if you change the seed!
    L = len(con_to_bit(seed))
    alp = 0.50
    method = 'haar'
    codes = decode_watermark(path_OG, path_W, L, alp, method)


