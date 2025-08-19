
# nodes/mix_colors_node.py
from ..lib.pixel_palette import PixelColor

class MixColorsNode:
    """
    Nœud ComfyUI pour mélanger deux couleurs PixelColor
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "color_a": ("PIXEL_COLOR", {
                    "tooltip": "Première couleur à mélanger"
                }),
                "color_b": ("PIXEL_COLOR", {
                    "tooltip": "Deuxième couleur à mélanger"
                }),
                "ratio": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "tooltip": "Ratio du mélange (0.0 = tout color_a, 1.0 = tout color_b)"
                }),
            }
        }

    RETURN_TYPES = ("PIXEL_COLOR",)
    RETURN_NAMES = ("mixed_color",)
    FUNCTION = "mix_colors"
    CATEGORY = "pixel_art/colors"

    def mix_colors(self, color_a: PixelColor, color_b: PixelColor, ratio: float = 0.5):
        """
        Mélange deux PixelColor en fonction d’un ratio
        """
        # On ne veut pas modifier color_a directement, donc on fait une copie
        base = PixelColor(
            r=color_a.r,
            g=color_a.g,
            b=color_a.b,
            name=color_a.name,
            color_space=color_a.color_space
        )
        mixed = base.mix_with(color_b, ratio)

        return (mixed,)
