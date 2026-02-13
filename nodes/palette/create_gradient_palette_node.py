# nodes/palette/create_gradient_palette_node.py
from ...lib.pixel_palette import PixelPalette
from ...lib.pixel_color import PixelColor


class CreateGradientPaletteNode:
    """
    Node ComfyUI pour créer une palette de dégradé entre deux couleurs
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "color_start": ("PIXEL_COLOR", {
                    "tooltip": "Couleur de départ du dégradé"
                }),
                "color_end": ("PIXEL_COLOR", {
                    "tooltip": "Couleur d'arrivée du dégradé"
                }),
                "num_colors": ("INT", {
                    "default": 8,
                    "min": 2,
                    "max": 256,
                    "step": 1,
                    "tooltip": "Nombre de couleurs dans le dégradé"
                }),
                "color_space": (["rgb", "hsv"], {
                    "default": "rgb",
                    "tooltip": "Espace de couleur pour l'interpolation"
                }),
            }
        }

    RETURN_TYPES = ("PIXEL_PALETTE",)
    RETURN_NAMES = ("gradient_palette",)
    FUNCTION = "create_gradient_palette"
    CATEGORY = "pixel_art/palette"

    def create_gradient_palette(self, color_start, color_end, num_colors=8, color_space="rgb"):
        """
        Crée une palette de dégradé entre deux couleurs

        Args:
            color_start: Couleur de départ
            color_end: Couleur d'arrivée
            num_colors: Nombre de couleurs
            color_space: "rgb" ou "hsv"

        Returns:
            PixelPalette: Palette contenant le dégradé
        """
        if not isinstance(color_start, PixelColor) or not isinstance(color_end, PixelColor):
            print("[CreateGradientPalette] ✗ Erreur: Couleurs invalides")
            return (PixelPalette(),)

        try:
            palette = PixelPalette.create_gradient_palette(
                color_start, color_end, num_colors, color_space
            )

            print(f"[CreateGradientPalette] ✓ Dégradé créé: {num_colors} couleurs ({color_space})")
            return (palette,)

        except Exception as e:
            print(f"[CreateGradientPalette] ✗ Erreur: {e}")
            return (PixelPalette(),)
