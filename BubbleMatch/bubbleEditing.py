import random
import cv2

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


    # return the result
    return copy
