# nodes/palette/replace_color_at_node.py
import sys
import os

# Add project root to sys.path for ComfyUI compatibility
current_file = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from lib.pixel_palette import PixelPalette, PixelColor

class ReplaceColorAtNode:
    """
    Node ComfyUI pour remplacer une couleur à un index spécifique dans une palette
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "palette": ("PIXEL_PALETTE", {
                    "tooltip": "Palette dans laquelle remplacer la couleur"
                }),
                "color": ("PIXEL_COLOR", {
                    "tooltip": "Nouvelle couleur à insérer"
                }),
                "index": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 255,  # Will be validated at runtime
                    "step": 1,
                    "tooltip": "Index de la couleur à remplacer (0 à palette.length-1)"
                }),
            }
        }

    RETURN_TYPES = ("PIXEL_PALETTE",)
    RETURN_NAMES = ("modified_palette",)
    FUNCTION = "replace_color_at"
    CATEGORY = "pixel_art/palette"

    def replace_color_at(self, palette: PixelPalette, color: PixelColor, index: int):
        """
        Remplace une couleur à l'index spécifié dans la palette

        Args:
            palette: La palette à modifier
            color: La nouvelle couleur
            index: L'index où remplacer la couleur

        Returns:
            PixelPalette: Nouvelle palette avec la couleur remplacée
        """
        # Validation de l'entrée
        if not isinstance(palette, PixelPalette):
            print("[ReplaceColorAt] ✗ Erreur: Objet palette invalide")
            return (palette,)  # Retourner l'original en cas d'erreur

        if not isinstance(color, PixelColor):
            print("[ReplaceColorAt] ✗ Erreur: Objet couleur invalide")
            return (palette,)

        # Validation de l'index
        if index < 0 or index >= len(palette.colors):
            print(f"[ReplaceColorAt] ✗ Erreur: Index {index} hors limites (0-{len(palette.colors)-1})")
            return (palette,)

        try:
            # Créer une copie de la palette pour éviter de modifier l'original
            import copy
            new_palette = copy.deepcopy(palette)

            # Remplacer la couleur à l'index spécifié
            new_palette.colors[index] = color

            print(f"[ReplaceColorAt] ✓ Couleur remplacée à l'index {index}: {color}")
            return (new_palette,)

        except Exception as e:
            print(f"[ReplaceColorAt] ✗ Erreur lors du remplacement: {e}")
            return (palette,)