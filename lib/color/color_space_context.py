
# lib/color/color_space_context.py
#
class ColorSpaceContext:
    def __init__(self, color, new_color_space):
        self.color = color
        self.new_color_space = new_color_space
        self.old_color_space = None

    def __enter__(self):
        self.old_color_space = self.color.color_space
        self.color.color_space = self.new_color_space
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.color.color_space = self.old_color_space
