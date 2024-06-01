class Bubble:
    def __init__(self, x, y, width, height, border_thickness):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.border_thickness = border_thickness

    def __repr__(self):
        return f"Speech Bubble: (x={self.x}, y={self.y}, width={self.width}, height={self.height})"
