# nodes/palette/insert_palette_node.py
import copy
from ...lib.pixel_palette import PixelPalette

class InsertPaletteNode:
    """
    Node ComfyUI pour insérer une palette dans une autre à un index donné
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "palette": ("PIXEL_PALETTE", {
                    "tooltip": "Palette de destination"
                }),
                "sub_palette": ("PIXEL_PALETTE", {
                    "tooltip": "Palette à insérer"
                }),
                "index": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 255,
                    "step": 1,
                    "tooltip": "Position d'insertion (0 = début)"
                }),
            }
        }

    RETURN_TYPES = ("PIXEL_PALETTE",)
    RETURN_NAMES = ("modified_palette",)
    FUNCTION = "insert_palette"
    CATEGORY = "pixel_art/palette"

    def insert_palette(self, palette: PixelPalette, sub_palette: PixelPalette, index: int):
        """
        Insère une palette dans une autre à l'index spécifié
        """
        if not isinstance(palette, PixelPalette) or not isinstance(sub_palette, PixelPalette):
            print("[InsertPalette] Erreur: Objet palette invalide")
            return (palette,)

        try:
            result = palette.insert_palette(sub_palette, index)
            print(f"[InsertPalette] {len(sub_palette)} couleurs insérées à l'index {index}")
            return (result,)

        except IndexError as e:
            print(f"[InsertPalette] Erreur: {e}")
            return (copy.deepcopy(palette),)
