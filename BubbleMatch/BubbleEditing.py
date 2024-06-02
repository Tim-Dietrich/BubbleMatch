import random
import cv2
import numpy as np

from PIL import Image, ImageFont, ImageDraw

from BubbleMatch import ImageProcessing, Parameters
from BubbleMatch.Bubble import Bubble
from BubbleMatch.DatasetPreparation import create_xml
from BubbleMatch.ShapeCreator import create_ellipse


# Generates all bubble images from a provided source image
def generate_data(source_image, path):
    print(source_image.shape)
    generated_images_per_source = 10
    generated_images = []

    # apply manga filter to source image
    source_image = ImageProcessing.manga_filter(source_image)

    # iterate and create bubble images
    for index in range(generated_images_per_source):
        # TODO: change this to a normal distribution or whatever suits us better
        bubble_count = random.randrange(1, 3)
        generated_images.append(generate_bubble_image(source_image, bubble_count, index, path))

    for img in generated_images:
        cv2.imshow("img", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


# image information: image.shape[] = {height, width, channels}

# Takes a given source image and adds bubbles to it
# returns the modified image
def generate_bubble_image(source_image, bubble_count, index, path):
    # step 1: create bubbles
    bubbles = []
    for i in range(bubble_count):
        height = int(source_image.shape[0] * random.uniform(0.1, 0.3))
        width = random.randrange(int(height * 0.1), int(height * 0.75))
        x = random.randrange(0 + width, source_image.shape[1] - width)
        y = random.randrange(0 + height, source_image.shape[0] - height)
        border_thickness = random.randrange(3, 7)
        bubbles.append(Bubble(x, y, width, height, border_thickness))

    # create new copy
    modified_image = source_image.copy()

    # step 2: Add black bubbles
    for bubble in bubbles:
        # draw black background for borders

        modified_image = create_ellipse(
            modified_image,
            bubble.x,
            bubble.y,
            bubble.height + bubble.border_thickness,
            bubble.width + bubble.border_thickness,
            Parameters.ELLIPSE_BORDER_COLOR
            )

    # step 3: Add white bubbles
    for bubble in bubbles:
        # draw white inside
        modified_image = create_ellipse(modified_image, bubble.x, bubble.y, bubble.height, bubble.width, Parameters.ELLIPSE_INSIDE_COLOR)
        print("Bubble data: " + str(bubble))

    # step 4: Add text
    for bubble in bubbles:
        coordinates = (bubble.x - bubble.width / 2, bubble.y - bubble.height + 5)
        fontsize = random.randint(15, 45)
        modified_image = write_text(modified_image, coordinates, bubble.height, fontsize)

    # step 5: create XML for tensorflow
    write_to_xml(modified_image, bubbles, index, path)

    # step 6: write images to path
    file_name = str(index) + '.jpg'
    cv2.imwrite(path + file_name, modified_image)

    # return the result
    return modified_image


def write_to_xml(image, bubbles, index, path):
    # calculate box coordinates for xml generation
    coordinates = []
    bubble_type = 'speech_bubble'
    for bubble in bubbles:
        x_min = max(0, bubble.x - bubble.width - bubble.border_thickness)
        y_min = max(0, bubble.y - bubble.height - bubble.border_thickness)
        x_max = min(image.shape[1], bubble.x + bubble.width + bubble.border_thickness)
        y_max = min(image.shape[0], bubble.y + bubble.height + bubble.border_thickness)
        coordinates.append([bubble_type, x_min, y_min, x_max, y_max])

    create_xml(path=path, img=str(index), width=image.shape[1], height=image.shape[0], boxes=coordinates)


# Write text onto the given image. This uses PIL instead of OpenCV
# TODO: multi-line text for wider bubbles, reduce fontsize on bubbles that are too small
# WARNING: turn 'bubble' into a parameter instead of passing single values
def write_text(image, coordinates, height, fontsize):
    # get text
    excerpt = fetch_random_excerpt(50)
    print(excerpt)
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
        print(character, coordinates, x, coordinates[1] - x)
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
