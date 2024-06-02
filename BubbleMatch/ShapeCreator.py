import cv2
import numpy as np
import os


def create_ellipse(image, x, y, height, width, color):
    center_coordinates = (x, y)
    axes_length = (width, height)
    angle = 0
    start_angle = 0
    end_angle = 360
    # -1 fills the ellipse
    thickness = -1
    print(x, y, height, width, color)
    image = cv2.ellipse(image, center_coordinates, axes_length, angle, start_angle, end_angle, color, thickness)
    return image


# testing!!!
def create_triangle(x, y, height, width, color, image):
    pt1 = (150, 100)
    pt2 = (100, 200)
    pt3 = (200, 200)

    cv2.circle(image, pt1, 2, color, -1)
    cv2.circle(image, pt2, 2, color, -1)
    cv2.circle(image, pt3, 2, color, -1)

    triangle_cnt = np.array([pt1, pt2, pt3])

    image = cv2.drawContours(image, [triangle_cnt], 0, color, -1)
    return image


def test_bubble():
    assert os.path.exists(r'../files/sample.jpg')
    path = r'../files/sample.jpg'

    image = cv2.imread(path)

    # resize to fit dimensions
    dim = (1000, 750)
    image = cv2.resize(image, dim, interpolation=cv2.INTER_LINEAR)

    window_name = 'Sample Image'

    image = create_ellipse(image, 500, 500, 205, 105, (0, 0, 0))
    image = create_ellipse(image, 500, 500, 200, 100, (255, 255, 255))

    image = create_triangle(500, 500, 100, 100, (0, 255, 0), image)

    cv2.imshow(window_name, image)

    cv2.waitKey(0)

    cv2.destroyAllWindows()
