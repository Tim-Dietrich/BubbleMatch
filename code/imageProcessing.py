import os
import cv2
import random
from sampleBubble import create_elipse
import json


def image_generation_test():
    # get image TODO: replace with parameters
    assert os.path.exists(r'../files/image.jpg')
    image = cv2.imread(r'../files/image.jpg')

    # modify image
    modified_image = cartoon_test(image)

    # create path + write images to disk TODO: parameters
    image_name = 'sample1'
    path = r'../files/Output/' + image_name + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    cv2.imwrite(path + 'image_original.jpg', image)
    cv2.imwrite(path + 'image_processed.jpg', modified_image)

    # create text file TODO: parameters
    f = open(path + 'sample1.txt', 'w')

    # generate and save bubble versions
    bubble_count = 5
    for i in range(bubble_count):
        add_ellipsis_and_save(modified_image, path, i, f)
    f.close()


def add_ellipsis_and_save(image, path, idx, f):
    # image dimensions
    image_height = image.shape[0]
    image_width = image.shape[1]

    # define random position
    x = random.randint(50, image_width - 51)
    y = random.randint(50, image_height - 51)

    # define ranges for randomness
    max_w = image_width - x
    max_h = image_height - y

    # define width and height
    w = random.randint(50, max_w)
    h = random.randint(50, max_h)

    # modify image and create ellipses
    copy = image.copy()
    outline_thickness = random.randint(2, 7)
    copy = create_elipse(copy, x, y, w+outline_thickness, h+outline_thickness, (0, 0, 0))
    copy = create_elipse(copy, x, y, w, h, (255, 255, 255))

    # write to file
    file_name = str(idx) + '.jpg'
    cv2.imwrite(path + file_name, copy)

    # add annotation to text file
    annotation = {
        "name": file_name,
        "bubbleType": "single",
        "x": x,
        "y": y,
        "w": w,
        "h": h,
    }

    f.write(json.dumps(annotation) + "\n")

# Common online version, doesn't work that great and only combines images
# def cartoonize(image):
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#
#     blurImage = cv2.medianBlur(image, 1)
#
#     edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
#     # edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 9, 9)
#
#     color = cv2.bilateralFilter(image, 9, 200, 200)
#     # color = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
#
#     cv2.imshow('test', edges)
#
#     cartoon = cv2.bitwise_and(color, color, mask=edges)
#
#     # optional gray scaling
#     # cartoon = cv2.cvtColor(cartoon, cv2.COLOR_GRAY2BGR)
#
#     return cartoon


def cartoon_test(image, debug_windows=False):
    # convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # blur
    blur = cv2.GaussianBlur(gray, (0, 0), sigmaX=33, sigmaY=33)

    # raise contrast on the blurred image
    blur = cv2.addWeighted(blur, 2, blur, 0, 0)

    # divide
    divide = cv2.divide(gray, blur, scale=255)

    # otsu threshold
    # thresh = cv2.threshold(divide, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]

    # alternative: adaptive thresh
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

    # apply morphology
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    morph = cv2.cvtColor(morph, cv2.COLOR_GRAY2RGB)

    # display it if debug enabled
    if debug_windows:
        cv2.imshow("gray", gray)
        cv2.imshow("divide", divide)
        cv2.imshow("thresh", thresh)
        cv2.imshow("morph", morph)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return morph
