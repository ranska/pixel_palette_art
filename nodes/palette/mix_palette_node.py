# nodes/palette/mix_palette_node.py
from ...lib.pixel_palette import PixelPalette

class MixPaletteNode:
    """
    Node ComfyUI pour mixer deux palettes couleur par couleur
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "palette_a": ("PIXEL_PALETTE", {
                    "tooltip": "Première palette"
                }),
                "palette_b": ("PIXEL_PALETTE", {
                    "tooltip": "Deuxième palette"
                }),
                "ratio": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "tooltip": "Ratio du mélange (0.0 = tout A, 1.0 = tout B)"
                }),
                "color_space": (["rgb", "hsv"], {
                    "default": "rgb",
                    "tooltip": "Espace colorimétrique pour le mélange"
                }),
                "offset": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 255,
                    "step": 1,
                    "tooltip": "Décalage d'index pour la palette B"
                }),
            }
        }

    RETURN_TYPES = ("PIXEL_PALETTE",)
    RETURN_NAMES = ("mixed_palette",)
    FUNCTION = "mix_palettes"
    CATEGORY = "pixel_art/palette"

    def mix_palettes(self, palette_a: PixelPalette, palette_b: PixelPalette,
                     ratio: float = 0.5, color_space: str = "rgb", offset: int = 0):
        """
        Mixe deux palettes couleur par couleur
        """
        if not isinstance(palette_a, PixelPalette) or not isinstance(palette_b, PixelPalette):
            print("[MixPalette] Erreur: Objet palette invalide")
            return (palette_a,)

        result = palette_a.mix_with_palette(palette_b, ratio, color_space, offset)
        print(f"[MixPalette] Mix {color_space.upper()} ratio={ratio} offset={offset} → {len(result)} couleurs")
        return (result,)
