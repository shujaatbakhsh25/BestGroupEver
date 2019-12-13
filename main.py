import os
from DecoderV3 import *
from Watermark import *
from dotenv import load_dotenv
load_dotenv(os.path.join(os.getcwd(), '.env'))

# set_tesseract_executable()


def createImagePathPairs():
    """ This will return path pairs for original and watermarked images """
    originals = []
    watermarked = []
    users = createUserList()
    for user in users:
        for i in [f for f in os.listdir(os.path.join(os.getcwd(), 'src')) if f.endswith('.png')]:
            originals.append(os.path.join(os.getcwd(), 'src', i))
            watermarked.append(os.path.join(
                os.getcwd(), 'dest', f'{user[0]}', i))
    return list(zip(originals, watermarked))


if __name__ == "__main__":
    print("Creating directories and adding watermarks. Please wait.....")
    createUserList()
    makeUserDirectories()
    watermark()
    for i in createImagePathPairs():
        n = 3
        L = 21 *21
        alp = 0.50
        method = 'haar'
        print(f'\noriginal image ---> f{i[0]}\n')
        print(f'watermarked image ---> f{i[1]}\n')
        code = decode_watermark(i[0], i[1], L, alp, method, n)
        print(f'watermark read ---> {code}\n')
