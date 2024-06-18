import os
from os import listdir
from os.path import isfile, join
import cv2
from BubbleMatch.ImageEditing import generate_data
from BubbleMatch.Utils import print_progress_bar


# All functions for testing purposes only
def image_generation_test():
    # get image
    path = r'../files/Input/images'
    assert os.path.exists(path)
    only_files = [f for f in listdir(path) if isfile(join(path, f))]
    total_files = len(only_files)

    for idx, file in enumerate(only_files):
        curr_path = path + '/' + file
        image = cv2.imread(curr_path)

        # create path + write images to disk
        output_path = r'../files/Output/test01/'
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        image = normalize_image_dimensions(image)

        generate_data(image, output_path, idx)
        print_progress_bar(idx+1, total_files)


# 109 dimensions: 1,654 x 1,170
def normalize_image_dimensions(image):
    return cv2.resize(image, (1654, 1170))
