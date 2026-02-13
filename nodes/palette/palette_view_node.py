# nodes/palette/palette_view_node.py
import torch
import numpy as np

from ...lib.pixel_palette import PixelPalette
from ...lib.palette.palette_renderer import PaletteRenderer


class PaletteViewNode:
    """
    Node ComfyUI pour visualiser une palette comme image
    Supporte les layouts grille, horizontal et vertical
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "palette": ("PIXEL_PALETTE", {
                    "tooltip": "Palette à visualiser"
                }),
                "layout": (["grid", "horizontal", "vertical"], {
                    "default": "grid",
                    "tooltip": "Disposition : grille, bande horizontale ou verticale"
                }),
                "cell_size": ("INT", {
                    "default": 32,
                    "min": 8,
                    "max": 128,
                    "step": 4,
                    "tooltip": "Taille de chaque cellule en pixels"
                }),
                "columns": ("INT", {
                    "default": 8,
                    "min": 1,
                    "max": 64,
                    "step": 1,
                    "tooltip": "Nombre de colonnes (mode grille uniquement)"
                }),
            },
            "optional": {
                "show_names": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Afficher les noms des couleurs"
                }),
                "show_indices": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Afficher les indices des couleurs"
                }),
                "show_hex": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Afficher les valeurs hexadécimales"
                }),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "render_palette"
    CATEGORY = "pixel_art/output"

    def render_palette(self, palette, layout="grid", cell_size=32, columns=8,
                       show_names=False, show_indices=False, show_hex=False):
        """
        Génère une image de la palette

        Returns:
            Tensor IMAGE au format ComfyUI [batch, height, width, channels]
        """
        if not isinstance(palette, PixelPalette):
            print("[PaletteView] ✗ Erreur: Objet palette invalide")
            error_img = np.full((cell_size, cell_size, 3), [255, 0, 0], dtype=np.uint8)
            return (torch.from_numpy(error_img.astype(np.float32) / 255.0)[None,],)

        try:
            renderer = PaletteRenderer(palette)
            img = renderer.render(
                layout=layout,
                cell_size=cell_size,
                columns=columns,
                show_names=show_names,
                show_indices=show_indices,
                show_hex=show_hex,
            )

            # Conversion PIL -> numpy -> torch (format ComfyUI)
            img_array = np.array(img).astype(np.float32) / 255.0
            img_tensor = torch.from_numpy(img_array)[None,]

            print(f"[PaletteView] ✓ Image {img.width}x{img.height} ({layout}, "
                  f"{palette.color_count} couleurs)")
            return (img_tensor,)

        except Exception as e:
            print(f"[PaletteView] ✗ Erreur: {e}")
            error_img = np.full((cell_size, cell_size, 3), [255, 0, 0], dtype=np.uint8)
            return (torch.from_numpy(error_img.astype(np.float32) / 255.0)[None,],)
