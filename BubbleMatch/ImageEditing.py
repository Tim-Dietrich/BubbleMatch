import os
import random
import cv2
import numpy as np

from PIL import Image, ImageFont, ImageDraw

from BubbleMatch import ImageProcessing, Parameters
from BubbleMatch.Objects.Bubble import Bubble
from BubbleMatch.DatasetPreparation import create_xml
from BubbleMatch.Objects.Rectangle import Rectangle
from BubbleMatch.Parameters import OBJECT_TEXT_COLOR


# Generates all bubble images from a provided source image
def generate_data(source_image, path, idx):
    generated_images_per_source = 10
    generated_images = []

    # apply manga filter to source image
    source_image = ImageProcessing.manga_filter3(source_image)

    # iterate and create bubble images
    for index in range(generated_images_per_source):
        # object_count = random.randrange(1, 4)
        object_count = 1
        generated_images.append(generate_modified_image(source_image, object_count, index, path, idx))

    '''for img in generated_images:
        cv2.imshow("img", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()'''


# image information: image.shape[] = {height, width, channels}

def create_objects(source_image, object_count, object_type: int):
    # WARNING: FOR DEBUG ONLY
    # object_type = 1
    objects = []
    for i in range(object_count):
        border_thickness = random.randrange(3, 7)
        match object_type:
            case 0:
                height = int(source_image.shape[0] * random.uniform(0.1, 0.3))
                width = random.randrange(int(height * 0.3), int(height * 0.75))
                x = random.randrange(0 + width, source_image.shape[1] - width)
                y = random.randrange(0 + height, source_image.shape[0] - height)
                objects.append(Bubble(x, y, width, height, border_thickness))
            case 1:
                # image dimensions
                image_height = source_image.shape[0]
                image_width = source_image.shape[1]

                width_buffer = image_width // 10
                height_buffer = image_height // 10

                # randomize upper left point of rectangle
                x_min = random.randint(0, image_width - width_buffer)
                y_min = random.randint(0, height_buffer)

                # define lower right point of rectangle
                y_max = random.randint(y_min + 2 * height_buffer, image_height)
                y_diff = y_max - y_min
                x_max = random.randint(x_min + width_buffer, min(x_min + y_diff, image_width))
                # print("Square dimensions", x_min, y_min, x_max, y_max)
                objects.append(Rectangle(x_min, x_max, y_min, y_max, border_thickness))
            case 2:
                pass
    return objects


# Takes a given source image and adds bubbles to it
# returns the modified image
def generate_modified_image(source_image, object_count, index, path, idx):
    # step 1: create objects
    # 0 -> Ellipse
    # 1 -> Rectangle
    # 2 -> Polygon
    object_type = random.randint(0, 1)
    objects = create_objects(source_image, object_count, object_type)

    # create new copy
    modified_image = source_image.copy()

    # step 2: Add black objects
    for target_object in objects:
        # draw black background for borders
        modified_image = target_object.draw_object(modified_image, Parameters.OBJECT_BORDER_COLOR, True)

    # step 3: Add white objects
    for target_object in objects:
        # draw white inside
        modified_image = target_object.draw_object(modified_image, Parameters.OBJECT_INSIDE_COLOR, False)
        # print("Bubble data: " + str(target_object))

    # step 4: Add text
    for target_object in objects:
        modified_image = write_text(modified_image, target_object)

    # step 5: create XML for tensorflow
    file_index = str(idx) + '_' + str(index)
    write_to_xml(modified_image, objects, path, file_index)

    # step 6: write images to path
    file_name = file_index + '.jpg'
    cv2.imwrite(path + file_name, modified_image)

    # return the result
    return modified_image


def write_to_xml(image, bubbles, path, file_index):
    # calculate box coordinates for xml generation
    coordinates = []
    bubble_type = 'speech_bubble'
    for bubble in bubbles:
        curr_coordinates = bubble.get_xml_coordinates(image)
        coordinates.append(curr_coordinates)
        # coordinates.append([bubble_type, x_min, y_min, x_max, y_max])

    create_xml(path=path, file_index=file_index, width=image.shape[1], height=image.shape[0], boxes=coordinates)


# Write text onto the given image. This uses PIL instead of OpenCV
# TODO: multi-line text for wider bubbles, reduce fontsize on bubbles that are too small
# WARNING: turn 'bubble' into a parameter instead of passing single values
def write_text(image, target_object):
    # fetch text
    excerpt = fetch_random_excerpt(200)

    # get coordinates
    coordinates = target_object.get_text_coordinates()

    # get writable dimensions
    height = target_object.height
    width = target_object.width

    # adapt existing dimensions to better suit our text filling
    if isinstance(target_object, Bubble):
        val = int(height * 0.15)
        height = height * 2 - val * 2
        coordinates[1] += val
    elif isinstance(target_object, Rectangle):
        height = height - int(height * 0.01) * 2
        width = width - int(width * 0.01) * 2

    # calculate fitting fontsize
    fontsize = random.randint(25, 65)
    projected_fontsize = int(fontsize * (1 + ((height * width) / 1000000)))
    fontsize = projected_fontsize

    # create PIL image
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(image)

    # Draw non-ascii text onto image, using Yu Goth B
    font_path = "C:\\Windows\\Fonts\\YuGothB.ttc"
    assert os.path.exists(font_path)

    font = ImageFont.truetype(font_path, fontsize)
    draw = ImageDraw.Draw(pil_image)

    # iterate over excerpt and add characters vertically
    x = 0
    y = 0
    for character in excerpt:
        draw.text((coordinates[0] + y, coordinates[1] + x), character, fill=OBJECT_TEXT_COLOR, stroke_fill=10, font=font)
        x += fontsize
        if x > height - fontsize:
            y += fontsize
            x = 0
            if y > width - fontsize:
                break

    image = np.asarray(pil_image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return image


# Gets a random excerpt from the lorem ipsum file
def fetch_random_excerpt(excerpt_length=100):
    with open("../resources/lorem_ipsum.txt", 'r', encoding='utf-8') as file:
        text = file.read()

    if len(text) <= excerpt_length:
        return text

    start_index = random.randint(0, len(text) - excerpt_length)
    return text[start_index:start_index + excerpt_length]
