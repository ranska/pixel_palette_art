# nodes/palette_formatter_node.py
from ..lib import PixelPalette

class PaletteFormatterNode:
    """
    Node dédié au formatage des palettes
    Responsabilité unique: formatage de sortie
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "palette": ("PIXEL_PALETTE",),
                "format_type": (["rgb", "hex", "raw"], {"default": "rgb"}),
            },
            "optional": {
                "separator": ("STRING", {"default": "\n"}),
                "include_header": ("BOOLEAN", {"default": True}),
                "include_names": ("BOOLEAN", {"default": True}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("formatted_text",)
    FUNCTION = "format_palette"
    CATEGORY = "pixel_art/output"
    
    def format_palette(self, palette, format_type="rgb", separator="\n", include_header=True, include_names=True):
        """
        Formate une palette - utilise les méthodes de l'objet
        """
        if not isinstance(palette, PixelPalette):
            return ("Erreur: Objet palette invalide",)
        
        # L'objet se formate lui-même
        formatted_output = palette.to_formatted_string(
            format_type=format_type,
            separator=separator,
            include_header=include_header
        )
        
        return (formatted_output,)
