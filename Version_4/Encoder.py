from PIL import Image
import os

os.chdir("F:/Downloads/595/")

def watermarked_image(input_image, output_image, watermark_image, position):
    base_image = Image.open(input_image)
    watermark = Image.open(watermark_image)

    base_image.paste(watermark, position, mask = watermark)
    base_image.show()
    base_image.save(output_image)

if __name__ == '__main__':
    img_orgnl = input("original image: ")
    img_wtmrk = input("watermark image: ")
    watermarked_image(img_orgnl, 'output.jpg', img_wtmrk, position = (0, 0))