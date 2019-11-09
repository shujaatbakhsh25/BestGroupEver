# Digital Watermarking 
## BestGroupEver - Midterm Project | Financial Technology (FE595)

### Overview
This is the code for digital watermarking of images. We have built a model which embeds watermark to images and decodes it, that can be used to trace the original user with whom it was shared. This technology helps in protecting the author's work and rights, and ultimately preventing piracy.

### Requirements
1. `pip install -r requirements.txt`
2. Download Tesseract [here](https://github.com/tesseract-ocr/tesseract/wiki/Downloads)

### Usage
Once dependencies are installed, download the project directory and just run this.

`python3 main.py`

That's it! Program loads the orginal images from `src` folder and stores the watermarked images to `dest` folder consisting of individual users. We can identify the original user with which the image file was shared by reading the watermarked image.
