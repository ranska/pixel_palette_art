
# nodes/palette_formatter_node.py
from ..lib import PixelPalette

class PaletteFormatterNode:
    """
    Nœud dédié au formatage des palettes
    Responsabilité unique: interface de formatage pour ComfyUI
    Toute la logique de formatage est dans PixelPalette
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "palette": ("PIXEL_PALETTE",),
                "format_type": (["rgb", "hex", "raw", "gimp"], {"default": "rgb"}),
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
    
    def format_palette(self, palette, format_type="rgb", separator="\n", 
                      include_header=True, include_names=True):
        """
        Formate une palette selon les paramètres fournis
        Interface simple vers la méthode métier de PixelPalette
        """
        # Validation de l'entrée
        if not isinstance(palette, PixelPalette):
            print("[PaletteFormatter] ✗ Erreur: Objet palette invalide")
            return ("# Erreur: Objet palette invalide",)
        
        try:
            # Délégation complète à la classe métier
            formatted_output = palette.to_formatted_string(
                format_type=format_type,
                separator=separator,
                include_header=include_header,
                include_names=include_names
            )
            
            # Log de succès
            print(f"[PaletteFormatter] ✓ Palette formatée: '{palette.name}' "
                  f"({palette.color_count} couleurs, format: {format_type})")
            
            return (formatted_output,)
            
        except Exception as e:
            # Gestion d'erreur avec sortie valide
            error_msg = f"# Erreur de formatage: {str(e)}"
            print(f"[PaletteFormatter] ✗ Erreur: {e}")
            return (error_msg,)

