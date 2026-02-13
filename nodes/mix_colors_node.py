
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
                "color_space": (["rgb", "hsv"], {
                    "default": "rgb",
                    "tooltip": "Espace colorimétrique utilisé pour le mélange"
                }),
            }
        }

    RETURN_TYPES = ("PIXEL_COLOR",)
    RETURN_NAMES = ("mixed_color",)
    FUNCTION     = "mix_colors"
    CATEGORY     = "pixel_art/colors"

    def mix_colors(self, color_a: PixelColor, color_b: PixelColor, ratio: float = 0.5, color_space: str = "rgb"):
        """
        Mélange deux PixelColor en fonction d’un ratio et d’un espace colorimétrique choisi
        """
        base = PixelColor(
            r=color_a.r,
            g=color_a.g,
            b=color_a.b,
            name=color_a.name,
            color_space=color_space
        )
        #
        with base.using_color_space(color_space):
            mixed = base.mix_with(color_b, ratio)

        return (mixed,)
