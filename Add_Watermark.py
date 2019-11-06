'''
This file should add a barium pill, i.e. a watermark, that we can use to trace the follow of a picture.
Author: Will Long
Date: 10/26/2019
'''


import numpy as np
import csv
from PIL import Image, ImageDraw, ImageFont


def add_watermark(path, seed, pos):
    '''
    This function should add a watermark to the picture.
    :param path: String, the file path of the picture
    :param seed: String, the code used to generate the watermark
    :param pos: A 2D point on [0,1], should be the off set you want for the watermark, i.e. [0.5,0.5] would be at the
    center
    :return: out: the watermarked image
    '''

    im = Image.open(path).convert("RGBA")
    #draw = ImageDraw.Draw(im)
    width, height = im.size
    wm = gen_watermark(seed, pos, width, height)
    out = Image.alpha_composite(im, wm)

    return out


def gen_watermark(seed, pos, width, height):
    '''
    This should generate the actually watermark.
    :param seed: String, the code used to generate the watermark
    :param pos:  A 2D point on [0,1], should be the off set you want for the watermark
    :param width: Int, width of the og image
    :param height: Int, height of the og image
    :return: the watermark we want to add
    '''

    txt = Image.new('RGBA', (width, height),  (255, 255, 255, 0))
    # you might want to edit this part.
    fnt = ImageFont.truetype('arial.ttf', 40)
    d = ImageDraw.Draw(txt)
    d_w = np.ceil(width * pos[0])
    d_h = np.ceil(height * pos[1])
    d.text((d_w, d_h), seed, font=fnt, fill=(255, 255, 255, 255))
    return txt


if __name__ == "__main__":
    image_path = 'src/OG.png'
    code = 'AA0010'
    pos = [0.5, 0.5]
    image_wm = add_watermark(image_path, code, pos)
    image_wm.save('dist/test_text.png')
