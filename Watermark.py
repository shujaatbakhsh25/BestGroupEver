import os
import csv
import shutil
from BestGroupEver.Add_WatermarkV3 import *


def createUserList(user_path, user_file):
    """ Creates a list of tuples with username and code from csv file """
    users = []

    with open(os.path.join(os.getcwd(), user_path, user_file)) as infile:
        reader = csv.reader(infile, delimiter=',')
        next(reader, None)
        for i in reader:
            users.append((i[0], i[2]))
    return users


def makeUserDirectories(user_path, user_file, dest_path):
    """ Makes user directories in the dest folder. 
    Deletes present directories and creates new ones."""
    try:
        shutil.rmtree(os.path.join(os.getcwd(), dest_path))
    except Exception as e:
        print(e)
        pass
    os.mkdir(os.path.join(os.getcwd(), dest_path))
    users = createUserList(user_path, user_file)
    for i in users:
        try:
            os.mkdir(os.path.join(os.getcwd(), dest_path, f'{i[0]}'))
        except FileExistsError as e:
            pass


def watermark(user_path, user_file, dest_path, pic_path, pic_type, alp, method, n):
    """ Watermarks all the images in src folder for each user.
    Puts the watermarked image in the dest folder under each user's directory. """
    users = createUserList(user_path, user_file)
    for i in [f for f in os.listdir(os.path.join(os.getcwd(), pic_path)) if f.endswith(pic_type)]:
        image_path = os.path.join(os.getcwd(), pic_path, i)
        seed = list(map(lambda x: x[1], users))
        image_wm = add_watermark(image_path, seed, alp, method, n)
        for j in range(len(image_wm)):
            cv2.imwrite(f'{dest_path}/{users[j][0]}/{i.split(".")[0]}{pic_type}', image_wm[j])


if __name__ == "__main__":
    user_path = 'BestGroupEver/src'
    user_file = 'users.csv'
    dest_path = 'BestGroupEver/dest'
    pic_path = 'BestGroupEver/src'
    pic_type = '.png'
    alp = 0.5
    method = 'haar'
    n = 3
    createUserList(user_path, user_file)
    makeUserDirectories(user_path, user_file, dest_path)
    watermark(user_path, user_file, dest_path, pic_path, pic_type, alp, method, n)
