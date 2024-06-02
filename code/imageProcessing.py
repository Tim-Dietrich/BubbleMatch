import os
import cv2
import random

import numpy as np

from sampleBubble import create_elipse
import json
from datasetPreparation import create_xml


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
    bubble_count = 20
    for i in range(bubble_count):
        # add_ellipsis_and_save(modified_image, path, i, f)
        # add_rectangle_and_save(modified_image, path, i, f)
        add_polygon_and_save(modified_image, path, i, f)
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

    # calculate box coordinates for xml generation
    coordinates = []
    bubble_type = 'speech_bubble'
    xmin = max(0, x-w)
    ymin = max(0, y-h)
    xmax = min(image_width, x+w)
    ymax = min(image_height, y+h)
    coordinates.append([bubble_type, xmin, ymin, xmax, ymax])

    create_xml(path=path, img=str(idx), width=image_width, height=image_height, boxes=coordinates)

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


def add_rectangle_and_save(image, path, idx, f):
    # image dimensions
    image_height = image.shape[0]
    image_width = image.shape[1]

    width_buffer = image_width//10
    height_buffer = image_height//10

    # randomize upper left point of rectangle
    x_min = random.randint(0, image_width - width_buffer)
    y_min = random.randint(0, image_height - height_buffer)

    # define lower right point of rectangle
    x_max = random.randint(x_min + width_buffer, image_width)
    y_max = random.randint(y_min + height_buffer, image_height)

    copy = image.copy()
    outline_thickness = random.randint(2, 7)
    copy = cv2.rectangle(copy, (x_min, y_min), (x_max, y_max), (0, 0, 0), -1)
    copy = cv2.rectangle(copy, (x_min + outline_thickness, y_min + outline_thickness),
                         (x_max - outline_thickness, y_max - outline_thickness), (255, 255, 255), -1)

    # write to file
    file = 'rect_' + str(idx)
    file_name = file + '.jpg'
    cv2.imwrite(path + file_name, copy)

    coordinates = [['speech_bubble', x_min, y_min, x_max, y_max]]
    create_xml(path=path, img=file, width=image_width, height=image_height, boxes=coordinates)


def add_polygon_and_save(image, path, idx, f):
    # image dimensions
    image_height = image.shape[0]
    image_width = image.shape[1]

    # buffer values to avoid speech bubble out of frame
    x_buffer = 100
    y_buffer = 200

    # define offsets for position
    x_offset = random.randint(0, image_width - x_buffer)
    y_offset = random.randint(0, image_height - y_buffer)

    # define standard polygon
    basic_polygon = np.array([[100, 100], [140, 130], [160, 200], [140, 240], [100, 270], [60, 240], [40, 200], [60, 130]], np.int32)

    # create copy for randomization
    curr_polygon = basic_polygon.copy()

    # randomize each point
    for i, vertex in enumerate(curr_polygon):
        vertex[0] = vertex[0] + random.randint(-10, 10) + x_offset
        vertex[1] = vertex[1] + random.randint(-10, 10) + y_offset

    # draw polygon
    copy = image.copy()
    cv2.fillPoly(copy,  [curr_polygon], (255, 255, 255))
    cv2.polylines(copy, [curr_polygon], True, (0, 0, 0), thickness=5)

    # save file
    file = 'poly_' + str(idx)
    file_name = file + '.jpg'
    cv2.imwrite(path + file_name, copy)

    # get inner boundaries for text
    inner_x_min = max(int(curr_polygon[5][0]), int(curr_polygon[7][0]))
    inner_y_min = max(int(curr_polygon[1][1]), int(curr_polygon[7][1]))
    inner_x_max = min(int(curr_polygon[1][0]), int(curr_polygon[3][0]))
    inner_y_max = min(int(curr_polygon[3][1]), int(curr_polygon[5][1]))

    # get outer boundaries for labeling
    x_min = max(int(curr_polygon[6][0]), 0)
    y_min = max(int(curr_polygon[0][1]), 0)
    x_max = min(int(curr_polygon[2][0]), image_width)
    y_max = min(int(curr_polygon[4][1]), image_height)

    coordinates = [['speech_bubble', x_min, y_min, x_max, y_max]]
    create_xml(path=path, img=file, width=image_width, height=image_height, boxes=coordinates)


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

    contrast = gray.copy()
    for x in range(len(contrast)):
        for y in range(len(contrast[x])):
            if contrast[x][y] < 125:
                contrast[x][y] = 0
            else:
                contrast[x][y] = 255

    # contours
    contours, hierarchy = cv2.findContours(contrast, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # print(len(contours))
    cnt = sorted(contours, key=cv2.contourArea, reverse=True)[:200]
    mask = np.zeros(gray.shape, gray.dtype)
    masked = cv2.drawContours(mask, cnt, -1, (255, 255, 255), -1)

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
        #cv2.imshow("divide", divide)
        cv2.imshow("thresh", thresh)
        #cv2.imshow("morph", morph)
        cv2.imshow("contours", masked)
        cv2.imshow("contrast", contrast)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return morph
