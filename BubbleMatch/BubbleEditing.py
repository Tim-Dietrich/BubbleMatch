import random
import cv2
import numpy as np

from PIL import Image, ImageFont, ImageDraw

from BubbleMatch import ImageProcessing, Parameters
from BubbleMatch.Bubble import Bubble
from BubbleMatch.DatasetPreparation import create_xml
from BubbleMatch.Square import Square


# Generates all bubble images from a provided source image
def generate_data(source_image, path, idx):
    print(idx)
    # print(source_image.shape)
    generated_images_per_source = 10
    generated_images = []

    # apply manga filter to source image
    source_image = ImageProcessing.manga_filter(source_image)

    # iterate and create bubble images
    for index in range(generated_images_per_source):
        # TODO: change this to a normal distribution or whatever suits us better
        bubble_count = random.randrange(1, 3)
        generated_images.append(generate_modified_image(source_image, bubble_count, index, path, idx))

    '''for img in generated_images:
        cv2.imshow("img", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()'''


# image information: image.shape[] = {height, width, channels}

def create_objects(source_image, object_count, object_type: int):
    objects = []
    for i in range(object_count):
        border_thickness = random.randrange(3, 7)
        match object_type:
            case 0:
                height = int(source_image.shape[0] * random.uniform(0.1, 0.3))
                width = random.randrange(int(height * 0.1), int(height * 0.75))
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
                objects.append(Square(x_min, x_max, y_min, y_max, border_thickness))
            case 2: pass
        return objects


# Takes a given source image and adds bubbles to it
# returns the modified image
def generate_modified_image(source_image, object_count, index, path, idx):
    # step 0: randomize target_object type
    bubble_type = "Bubble"

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
        modified_image = target_object.draw_object(modified_image, Parameters.ELLIPSE_BORDER_COLOR, True)

    # step 3: Add white objects
    for target_object in objects:
        # draw white inside
        modified_image = target_object.draw_object(modified_image, Parameters.ELLIPSE_INSIDE_COLOR, False)
        # print("Bubble data: " + str(target_object))

    # step 4: Add text
    for target_object in objects:
        coordinates = target_object.get_text_coordinates()
        # scaled_size = source_image[1]
        fontsize = random.randint(15, 45)
        modified_image = write_text(modified_image, coordinates, target_object.height, fontsize)

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
def write_text(image, coordinates, height, fontsize):
    # get text
    excerpt = fetch_random_excerpt(50)
    # print(excerpt)
    # create PIL image
    # image = np.zeros((100, 950, 3), dtype=np.uint8)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(image)

    # Draw non-ascii text onto image
    font = ImageFont.truetype("C:\\Windows\\Fonts\\YuGothB.ttc", fontsize)
    draw = ImageDraw.Draw(pil_image)

    # iterate over excerpt and add characters vertically
    x = 0
    for character in excerpt:
        # print(character, coordinates, x, coordinates[1] - x)
        draw.text((coordinates[0], coordinates[1] + x), character, fill=(0, 0, 0), stroke_fill=10, font=font)
        x = x + fontsize
        if x > height * 2 - fontsize:
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
