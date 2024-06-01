import os
import cv2
from BubbleMatch.bubbleEditing import generate_data


# All functions for testing purposes only
def image_generation_test():
    # get image TODO: replace with parameters
    assert os.path.exists(r'../files/image.jpg')
    image = cv2.imread(r'../files/image.jpg')

    # create path + write images to disk TODO: parameters
    image_name = 'sample1'
    path = r'../files/Output/' + image_name + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    cv2.imwrite(path + 'image_original.jpg', image)

    generate_data(image, path)

    # generate and save bubble versions
    # generated_images_per_source = 5
    # for i in range(generated_images_per_source):
    #     add_ellipsis_and_save(modified_image, path, i)


# def add_ellipsis_and_save(image, path, idx):
#     # image dimensions
#     image_height = image.shape[0]
#     image_width = image.shape[1]
#
#     # define random position
#     x = random.randint(50, image_width - 51)
#     y = random.randint(50, image_height - 51)
#
#     # define ranges for randomness
#     max_w = image_width - x
#     max_h = image_height - y
#
#     # define width and height
#     w = random.randint(50, max_w)
#     h = random.randint(50, max_h)
#
#     # modify image and create ellipses
#     copy = image.copy()
#     outline_thickness = random.randint(2, 7)
#     copy = create_elipse(copy, x, y, w + outline_thickness, h + outline_thickness, (0, 0, 0))
#     copy = create_elipse(copy, x, y, w, h, (255, 255, 255))
#
#     # write to file
#     file_name = str(idx) + '.jpg'
#     cv2.imwrite(path + file_name, copy)
#
#     # calculate box coordinates for xml generation
#     coordinates = []
#     bubble_type = 'speech_bubble'
#     xmin = max(0, x - w)
#     ymin = max(0, y - h)
#     xmax = min(image_width, x + w)
#     ymax = min(image_height, y + h)
#     coordinates.append([bubble_type, xmin, ymin, xmax, ymax])
#
#     create_xml(path=path, img=str(idx), width=image_width, height=image_height, boxes=coordinates)

