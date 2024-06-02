from BubbleMatch.ShapeCreator import create_square


class Square():
    def __init__(self, x_min, x_max, y_min, y_max, border_thickness):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.height = y_max - y_min
        self.border_thickness = border_thickness
        self.bubble_type = 'speech_bubble'

    def __repr__(self):
        return f"Square: (x_min={self.x_min}, y_min={self.y_min}, x_max={self.x_max}, y_max={self.y_max})"

    def draw_object(self, image, color, is_outline):
        if is_outline:
            x_min = self.x_min
            y_min = self.y_min
            x_max = self.x_max
            y_max = self.y_max
        else:
            x_min = self.x_min + self.border_thickness
            y_min = self.y_min + self.border_thickness
            x_max = self.x_max - self.border_thickness
            y_max = self.y_max - self.border_thickness

        return create_square(
            image,
            x_min,
            x_max,
            y_min,
            y_max,
            color
        )

    def get_text_coordinates(self):
        return (self.x_min + self.x_max) / 2, self.y_min + 5

    def get_xml_coordinates(self, image):
        return [self.bubble_type, self.x_min, self.y_min, self.x_max, self.y_max]
