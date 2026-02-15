# nodes/palette/copy_subset_node.py
import copy
from ...lib.pixel_palette import PixelPalette

class CopySubsetNode:
    """
    Node ComfyUI pour extraire un sous-ensemble de couleurs d'une palette
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "palette": ("PIXEL_PALETTE", {
                    "tooltip": "Palette source"
                }),
                "start_index": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 255,
                    "step": 1,
                    "tooltip": "Index de début (inclusif)"
                }),
                "end_index": ("INT", {
                    "default": 3,
                    "min": 0,
                    "max": 255,
                    "step": 1,
                    "tooltip": "Index de fin (inclusif)"
                }),
            }
        }

    RETURN_TYPES = ("PIXEL_PALETTE",)
    RETURN_NAMES = ("subset",)
    FUNCTION = "copy_subset"
    CATEGORY = "pixel_art/palette"

    def copy_subset(self, palette: PixelPalette, start_index: int, end_index: int):
        """
        Extrait un sous-ensemble de couleurs de la palette
        """
        if not isinstance(palette, PixelPalette):
            print("[CopySubset] Erreur: Objet palette invalide")
            return (palette,)

        try:
            subset = palette.copy_subset(start_index, end_index)
            print(f"[CopySubset] Extraction [{start_index}:{end_index}] → {len(subset)} couleurs")
            return (subset,)

        except (ValueError, IndexError) as e:
            print(f"[CopySubset] Erreur: {e}")
            return (copy.deepcopy(palette),)
