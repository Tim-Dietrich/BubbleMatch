from BubbleMatch.ShapeCreator import create_ellipse
from BubbleMatch.Parameters import *


class Bubble:
    def __init__(self, x, y, width, height, border_thickness):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.border_thickness = border_thickness
        self.bubble_type = 'speech_bubble'

    def __repr__(self):
        return f"Speech Bubble: (x={self.x}, y={self.y}, width={self.width}, height={self.height})"

    def draw_object(self, image, color, is_outline):
        if is_outline:
            height = self.height + self.border_thickness
            width = self.width + self.border_thickness
        else:
            height = self.height
            width = self.width

        return create_ellipse(
            image,
            self.x,
            self.y,
            height,
            width,
            color
        )

    def get_text_coordinates(self):
        return self.x - self.width / 2, self.y - self.height + 5

    def get_xml_coordinates(self, image):
        x_min = max(0, self.x - self.width - self.border_thickness)
        y_min = max(0, self.y - self.height - self.border_thickness)
        x_max = min(image.shape[1], self.x + self.width + self.border_thickness)
        y_max = min(image.shape[0], self.y + self.height + self.border_thickness)

        return [self.bubble_type, x_min, y_min, x_max, y_max]
