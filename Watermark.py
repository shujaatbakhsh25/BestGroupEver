import os
import csv
import shutil
# from Add_WatermarkV3 import *


def createUserList():
    """ Creates a list of tuples with username and code from csv file """
    users = []

    with open(os.path.join(os.getcwd(), 'src', 'users.csv')) as infile:
        reader = csv.reader(infile, delimiter=',')
        next(reader, None)
        for i in reader:
            users.append((i[0], i[2].split('-')))
    return users


def makeUserDirectories():
    """ Makes user directories in the dest folder. 
    Deletes present directories and creates new ones."""
    try:
        shutil.rmtree(os.path.join(os.getcwd(), 'dest'))
    except Exception as e:
        print(e)
        pass
    os.mkdir(os.path.join(os.getcwd(), 'dest'))
    users = createUserList()
    for i in users:
        try:
            os.mkdir(os.path.join(os.getcwd(), 'dest', f'{i[0]}'))
        except FileExistsError as e:
            pass


# def watermark():
#     """ Watermarks all the images in src folder for each user.
#     Puts the watermarked image in the dest folder under each user's directory. """
#     users = createUserList()
#     for i in [f for f in os.listdir(os.path.join(os.getcwd(), 'src')) if f.endswith('.png')]:
#         for user in users:
#             image_path = os.path.join(os.getcwd(), 'src', i)
#             seed = user[1]
#             alp = 0.5
#             method = 'haar'
#             n = 3
#             image_wm = add_watermark(image_path, seed,alp,method, n)
#             for j in range(len(seed)):
#                 cv2.imwrite(os.path.join(os.getcwd(), 'dest', f'{user[0]}_{j}', i),image_wm[j])


if __name__ == "__main__":
    createUserList()
    makeUserDirectories()
    # watermark()
