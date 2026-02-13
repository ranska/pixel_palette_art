# nodes/palette/sort_palette_node.py
import sys
import os
import copy

# Ajout du chemin projet pour compatibilité ComfyUI
current_file = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from lib.pixel_palette import PixelPalette


class SortPaletteNode:
    """
    Node ComfyUI pour trier les couleurs d'une palette par teinte ou luminosité
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "palette": ("PIXEL_PALETTE", {
                    "tooltip": "Palette à trier"
                }),
                "sort_by": (["hue", "brightness"], {
                    "default": "hue",
                    "tooltip": "Critère de tri : teinte (hue) ou luminosité (brightness)"
                }),
            }
        }

    RETURN_TYPES = ("PIXEL_PALETTE",)
    RETURN_NAMES = ("sorted_palette",)
    FUNCTION = "sort_palette"
    CATEGORY = "pixel_art/palette"

    def sort_palette(self, palette, sort_by="hue"):
        """
        Trie les couleurs de la palette selon le critère choisi

        Args:
            palette: La palette à trier
            sort_by: "hue" ou "brightness"

        Returns:
            PixelPalette: Nouvelle palette triée
        """
        if not isinstance(palette, PixelPalette):
            print("[SortPalette] ✗ Erreur: Objet palette invalide")
            return (palette,)

        if palette.is_empty:
            print("[SortPalette] ✗ Palette vide, rien à trier")
            return (palette,)

        try:
            new_palette = copy.deepcopy(palette)

            if sort_by == "hue":
                new_palette.sort_by_hue()
            else:
                new_palette.sort_by_brightness()

            print(f"[SortPalette] ✓ Palette triée par {sort_by} ({new_palette.color_count} couleurs)")
            return (new_palette,)

        except Exception as e:
            print(f"[SortPalette] ✗ Erreur: {e}")
            return (palette,)
