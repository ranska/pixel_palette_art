# nodes/palette/gradient_between_node.py
import copy

from ...lib.pixel_palette import PixelPalette


class GradientBetweenNode:
    """
    Node ComfyUI pour créer un dégradé entre deux couleurs d'une palette existante
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "palette": ("PIXEL_PALETTE", {
                    "tooltip": "Palette contenant les couleurs de départ et d'arrivée"
                }),
                "index_start": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 255,
                    "step": 1,
                    "tooltip": "Index de la couleur de départ"
                }),
                "index_end": ("INT", {
                    "default": 2,
                    "min": 1,
                    "max": 255,
                    "step": 1,
                    "tooltip": "Index de la couleur d'arrivée"
                }),
                "color_space": (["rgb", "hsv"], {
                    "default": "rgb",
                    "tooltip": "Espace de couleur pour l'interpolation"
                }),
            }
        }

    RETURN_TYPES = ("PIXEL_PALETTE",)
    RETURN_NAMES = ("gradient_palette",)
    FUNCTION = "create_gradient_between"
    CATEGORY = "pixel_art/palette"

    def create_gradient_between(self, palette, index_start=0, index_end=2, color_space="rgb"):
        """
        Crée un dégradé entre deux couleurs aux indices donnés

        Args:
            palette: La palette source
            index_start: Index de la couleur de départ
            index_end: Index de la couleur d'arrivée
            color_space: "rgb" ou "hsv"

        Returns:
            PixelPalette: Nouvelle palette avec le dégradé appliqué
        """
        if not isinstance(palette, PixelPalette):
            print("[GradientBetween] ✗ Erreur: Objet palette invalide")
            return (palette,)

        if palette.is_empty:
            print("[GradientBetween] ✗ Palette vide")
            return (palette,)

        try:
            new_palette = copy.deepcopy(palette)
            new_palette.create_gradient(index_start, index_end, color_space)

            print(f"[GradientBetween] ✓ Dégradé créé entre index {index_start} et {index_end} ({color_space})")
            return (new_palette,)

        except (ValueError, IndexError) as e:
            print(f"[GradientBetween] ✗ Erreur: {e}")
            return (palette,)
        except Exception as e:
            print(f"[GradientBetween] ✗ Erreur inattendue: {e}")
            return (palette,)
