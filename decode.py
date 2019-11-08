import os
from decoder_test import *
from Watermark import *
from dotenv import load_dotenv
load_dotenv(os.path.join(os.getcwd(), '.env'))

set_tesseract_executable()


def createImagePathPairs():
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
    for i in createImagePathPairs():
        print(f'\noriginal image ---> f{i[0]}\n')
        print(f'watermarked image ---> f{i[1]}\n')
        code = decode_watermark(i[1])
        print(f'watermark read ---> {code}\n')
