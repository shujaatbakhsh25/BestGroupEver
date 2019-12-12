# Digital Watermarking

## BestGroupEver - Final Project | Financial Technology (FE595)

### Overview

This is the code for digital watermarking of images. We have built a model which embeds watermark to images and decodes it, which can be used to trace the original user with whom it was shared. This technology helps in protecting the author's work and rights, and ultimately preventing piracy.

### Requirements

1. `pip install -r requirements.txt`
2. Download Tesseract from [here](https://github.com/tesseract-ocr/tesseract/wiki/Downloads).
3. The project's root directory must have a `.env` file.
4. This `.env` file contains two variables `TESERRACT_EXECUTABLE` which should be assigned a value of complete path of the `tesseract.exe` file and `FONT_FILE` which should be assigned a value of the complete path of a `.ttf` font file (Arial used and preferred).
5. The environment variables must be assigned full pathnames as per the operating system.

### Usage

- Once dependencies are installed, download the project directory.
- Make sure the current directory is the project root directory.
- Put the images to be watermarked in `src` folder
- Run `python3 main.py`
- 
- That's it! Program loads the orginal images from `src` folder and stores the watermarked images to `dest` folder consisting of individual users. We can identify the original user with which the image file was shared by reading and decoding the watermarked image.
