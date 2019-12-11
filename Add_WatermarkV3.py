import numpy as np
import cv2
import pywt
import qrcode


def image_rec(coeffs, method):
    '''
    Reconstructing an image from the DWT coeffs in a usable way
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
    Embedding a bit stream into the array A.
    :param A: Array, the cover array
    :param w: List of {-1,1}, the bit stream
    :param alp: float on [0,1], the strength of the watermark
    :return: the watermarked array
    '''

    shape = A.shape
    A = A.flatten()
    L = len(w)
    A_cut = A
    ind = np.argpartition(A_cut, -L)[-L:]
    k = 0
    for i in ind:
        a = A[i] + alp * A[i] * w[k]
        A[i] = a
        k += 1
    A = np.reshape(A, shape)
    return A

def encode_QR(string):
    '''
    This function takes a string, encodes it in a QR code, flattens the QR code into a 1D Array, and returns that array.
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

def con_to_bit(string, n):
    '''
    This function converts a string into a binary array of {-1,1}
    :param string: String
    :param n: int
    :return: binary array of {-1,1}
    '''

    res1 = encode_QR(string).astype(str)
    res = []
    for i in range(n):
        res.extend(res1)
    a = []
    for i in range(len(res)):
        if res[i] == '1': a.append(1)
        if res[i] == '0': a.append(-1)

    return np.array(a)

def add_watermark(path, seed_list, alp, method, n):
    '''
    This function adds a watermark to the picture using DWT.
    :param path: String, the file path of the picture
    :param seed_list:  Array of Strings, the codes used to generate the watermark
    :param alp: float on [0,1], the strength of the watermark
    :param method: String, method used for the DWT
    :param n: int
    :return: Array, the watermarked images
    '''

    img = cv2.imread(path)
    colors = cv2.split(img) # You have to split the colors, otherwise DWT doesn't work.
    im_list = []


    for c in range(3):
        A = colors[c]
        coeffs = pywt.wavedec2(A, method)
        #Adding a loop to input multiple seeds

        for k in range(len(seed_list)):
            seed = seed_list[k]
            colors_w = []
            w = con_to_bit(seed, n)

            np_coeffs = [np.asarray(x) for x in coeffs]
            for j in range(len(coeffs[-2])):
                B = coeffs[-2][j]
                Bp = code_embed(B, w, alp)
                np_coeffs[-2][j] = Bp

            new_coeffs = [np_coeffs[0]]
            for i in range(1, len(np_coeffs)):
                new_coeffs.append((np_coeffs[i][0],np_coeffs[i][1], np_coeffs[i][2]))

            Aw = image_rec(new_coeffs, method)
            colors_w.append(Aw)
        img_w = cv2.merge(colors_w)
        im_list.append(img_w)
    #end of loop. It basically changes output from one image to a set of images

    return im_list

if __name__ == "__main__":
    image_path = 'Test.jpg'
    seed = ['ASDFGHJ', 'QWERTYY', 'ZXZXCVB', 'JKHUDNJ']
    alp = 0.5
    method = 'haar'
    n = 3
    image_watermarks = add_watermark(image_path, seed, alp, method, n)
    cv2.imwrite('Test_W.jpg', image_watermarks[0])
