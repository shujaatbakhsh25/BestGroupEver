# Digital Watermarking and Detection of Images

## BestGroupEver - Final Project | Financial Technology (FE595)

### Preety Vandana | William Long | Shujaat Bakhsh | Gaurav Nagal

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
- Run `python3 main.py` (`main.py` program calls `Add_WatermarkV3.py` to generate a list of unique images/arrays for the users defined in `users.csv`)
- That's it! Program loads all the orginal images from `src` folder and stores the watermarked images to `dest` folder consisting of individual users. 
- We can identify the original user with which the image file was shared by reading and decoding the watermarked image.

### Results

Here are some of the results comparing original and watermarked images

![](https://github.com/shujaatbakhsh25/BestGroupEver/blob/PreetyV-patch-2/src/Test6.png) ![](https://github.com/shujaatbakhsh25/BestGroupEver/blob/PreetyV-patch-2/dest/IC_Wiener3000/Test6.png)
<p align="center">
  <img src="https://github.com/shujaatbakhsh25/BestGroupEver/blob/PreetyV-patch-2/src/Test6.png" width="350" title="hover text">
  <img src="https://github.com/shujaatbakhsh25/BestGroupEver/blob/PreetyV-patch-2/src/Test6.png" width="350" alt="accessibility text">
</p>
