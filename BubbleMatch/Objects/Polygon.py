from BubbleMatch.ShapeCreator import create_polygon

class Polygon:
    def __init__(self, vertices, x_min, x_max, y_min, y_max, border_thickness):
        self.inner_y_max = None
        self.inner_y_min = None
        self.inner_x_max = None
        self.inner_x_min = None
        self.height = None
        self.width = None
        self.vertices = vertices
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.border_thickness = border_thickness
        self.bubble_type = 'speech_bubble'

    def draw_object(self, image, color, is_outline):
        return create_polygon(image, self.vertices, color, is_outline, self.border_thickness)

    def set_text_coordinates(self, inner_x_min, inner_x_max, inner_y_min, inner_y_max):
        self.inner_x_min = inner_x_min
        self.inner_x_max = inner_x_max
        self.inner_y_min = inner_y_min
        self.inner_y_max = inner_y_max
        self.height = self.inner_y_max - self.inner_y_min
        self.width = self.inner_x_max - self.inner_x_min

    def get_text_coordinates(self):
        return [self.inner_x_min + 5, self.inner_y_min + 5]

    def get_xml_coordinates(self, image):
        return [
            self.bubble_type,
            max(self.x_min - self.border_thickness, 0),
            max(self.y_min - self.border_thickness, 0),
            min(self.x_max + self.border_thickness, image.shape[1]),
            min(self.y_max + self.border_thickness, image.shape[0]),
        ]
