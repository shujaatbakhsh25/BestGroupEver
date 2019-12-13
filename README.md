# Digital Watermarking and Detection of Images

## BestGroupEver - Final Project | Financial Technology (FE595)

### Preety Vandana | William Long | Shujaat Bakhsh | Gaurav Nagal

### Overview

This is the code for digital watermarking of images. We have built a model which embeds watermark to images and decodes it, which can be used to trace the original user with whom it was shared. This technology helps in protecting the author's work and rights, and ultimately preventing piracy.

### Requirements

`pip install -r requirements.txt`

### Usage

- Once dependencies are installed, download the project directory.
- Make sure the current directory is the project root directory.
- Put the images to be watermarked in `src` folder
- Run `python3 main.py` (`main.py` program calls `Add_WatermarkV3.py` to generate a list of unique images/arrays for the users defined in `users.csv`)
- That's it! Program loads all the orginal images from `src` folder and stores the watermarked images to `dest` folder consisting of individual users. 
- We can identify the original user with which the image file was shared by reading and decoding the watermarked image.

### Results

Here are some of the results comparing original and watermarked images.
The left one is original image and right one is watermarked image.

<p align="center">
  <img src="https://github.com/shujaatbakhsh25/BestGroupEver/blob/master/src/Test6.png" width="350" title=" ">
  <img src="https://github.com/shujaatbakhsh25/BestGroupEver/blob/master/dest/IC_Wiener3000/Test6.png" width="350" alt=" ">
  <img src="https://github.com/shujaatbakhsh25/BestGroupEver/blob/master/src/Test7.png" width="350" title=" ">
  <img src="https://github.com/shujaatbakhsh25/BestGroupEver/blob/master/IC_Wiener3000/Test7.png" width="350" title=" ">
</p>
