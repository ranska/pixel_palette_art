# __init__.py (racine de votre extension)
"""
Extension ComfyUI pour les palettes de pixel art
"""

from .nodes import GimpPaletteLoaderNode, PaletteFormatterNode, PixelPaletteExtractorNode, CreateColorFromRGBNode, ColorFormatterNode, ColorPreviewNode
#  from . import PixelPaletteExtractor

# Configuration ComfyUI
NODE_CLASS_MAPPINGS = {
    "GimpPaletteLoader":      GimpPaletteLoaderNode,
    "PaletteFormatter":       PaletteFormatterNode,
    "PixelPaletteExtractor":  PixelPaletteExtractorNode,
    "CreateColorFromRGBNode": CreateColorFromRGBNode,
    "ColorFormatterNode":     ColorFormatterNode,
    "ColorPreviewNode":       ColorPreviewNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GimpPaletteLoader":      "GIMP Palette Loader",
    "PaletteFormatter":       "Palette Formatter",
    "PixelPaletteExtractor":  "Pixel Palette Extractor",
    "CreateColorFromRGBNode": "Create Color From RGB",
    "ColorFormatterNode":     "Color to formatted string",
    "ColorPreviewNode":       "Color to image",
}

# Métadonnées de l'extension
__version__     = "0.0.3"
__author__      = "Ranska"
__description__ = "Extension pour gérer les palettes de pixel art dans ComfyUI"

