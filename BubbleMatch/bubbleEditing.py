import random
import cv2
import numpy as np

from PIL import Image, ImageFont, ImageDraw

from BubbleMatch import imageProcessing, parameters
from BubbleMatch.Bubble import Bubble
from BubbleMatch.sampleBubble import create_elipse


# Generates all bubble images from a provided source image
def generate_data(source_image):
    print(source_image.shape)
    generated_images_per_source = 10
    generated_images = []

    # apply manga filter to source image
    source_image = imageProcessing.manga_filter(source_image)

    for i in range(generated_images_per_source):
        # INFO: change this for normal distribution or whatever suits us
        bubble_count = random.randrange(1, 3)
        generated_images.append(generate_bubble_image(source_image, bubble_count))

    for img in generated_images:
        cv2.imshow("img", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


# image information: image.shape[] = {height, width, channels}

# Takes a given source image and adds bubbles to it
# returns the modified image
def generate_bubble_image(source_image, bubble_count):
    # step 1: create bubbles
    bubbles = []
    for i in range(bubble_count):
        height = int(source_image.shape[0] * random.uniform(0.1, 0.3))
        width = random.randrange(int(height * 0.1), int(height * 0.75))
        x = random.randrange(0 + width, source_image.shape[1] - width)
        y = random.randrange(0 + height, source_image.shape[0] - height)
        bubbles.append(Bubble(x, y, width, height))

    # create new copy
    copy = source_image.copy()

    # step 2: Add black bubbles
    for bubble in bubbles:
        # draw black background for borders
        border_thickness = random.randrange(3, 7)
        copy = create_elipse(copy,
                             bubble.x,
                             bubble.y,
                             bubble.height + border_thickness,
                             bubble.width + border_thickness,
                             parameters.ELLIPSE_BORDER_COLOR
                             )

    # step 3: Add white bubbles
    for bubble in bubbles:
        # draw white inside
        copy = create_elipse(copy, bubble.x, bubble.y, bubble.height, bubble.width, parameters.ELLIPSE_INSIDE_COLOR)
        print("Bubble data: " + str(bubble))

    # step 4: Add text
    for bubble in bubbles:
        coordinates = (bubble.x - bubble.width / 2, bubble.y - bubble.height + 5)
        fontsize = random.randint(15, 45)
        copy = write_text(copy, coordinates, bubble.height, fontsize)

    # return the result
    return copy


# Write text onto the given image. This uses PIL instead of OpenCV
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
