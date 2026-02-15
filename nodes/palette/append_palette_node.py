# nodes/palette/append_palette_node.py
from ...lib.pixel_palette import PixelPalette

class AppendPaletteNode:
    """
    Node ComfyUI pour combiner deux palettes bout à bout
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "palette_a": ("PIXEL_PALETTE", {
                    "tooltip": "Première palette"
                }),
                "palette_b": ("PIXEL_PALETTE", {
                    "tooltip": "Palette à ajouter à la suite"
                }),
            }
        }

    RETURN_TYPES = ("PIXEL_PALETTE",)
    RETURN_NAMES = ("combined_palette",)
    FUNCTION = "append_palette"
    CATEGORY = "pixel_art/palette"

    def append_palette(self, palette_a: PixelPalette, palette_b: PixelPalette):
        """
        Combine deux palettes en une seule
        """
        if not isinstance(palette_a, PixelPalette) or not isinstance(palette_b, PixelPalette):
            print("[AppendPalette] Erreur: Objet palette invalide")
            return (palette_a,)

        result = palette_a.append_palette(palette_b)
        print(f"[AppendPalette] {len(palette_a)} + {len(palette_b)} → {len(result)} couleurs")
        return (result,)
