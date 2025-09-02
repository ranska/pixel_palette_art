# __init__.py (racine de votre extension)
"""
Extension ComfyUI pour les palettes de pixel art
"""

from .nodes import GimpPaletteLoaderNode, PaletteFormatterNode, PixelPaletteExtractorNode, CreateColorFromRGBNode, ColorFormatterNode, ColorPreviewNode, MixColorsNode

# Import ReplaceColorAtNode directly
import importlib.util
import os

ReplaceColorAtNode = None
try:
    # Try to import using importlib for better compatibility
    node_file = os.path.join(os.path.dirname(__file__), "nodes", "palette", "replace_color_at_node.py")
    spec = importlib.util.spec_from_file_location("replace_color_at_node", node_file)
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        ReplaceColorAtNode = module.ReplaceColorAtNode
except Exception as e:
    print(f"Warning: Could not import ReplaceColorAtNode: {e}")

NODE_CLASS_MAPPINGS = {
    "GimpPaletteLoader":      GimpPaletteLoaderNode,
    "PaletteFormatter":       PaletteFormatterNode,
    "PixelPaletteExtractor":  PixelPaletteExtractorNode,
    "CreateColorFromRGBNode": CreateColorFromRGBNode,
    "ColorFormatterNode":     ColorFormatterNode,
    "ColorPreviewNode":       ColorPreviewNode,
    "MixColorsNode":          MixColorsNode,
}

if ReplaceColorAtNode is not None:
    NODE_CLASS_MAPPINGS["ReplaceColorAtNode"] = ReplaceColorAtNode

NODE_DISPLAY_NAME_MAPPINGS = {
    "GimpPaletteLoader":      "GIMP Palette Loader",
    "PaletteFormatter":       "Palette Formatter",
    "PixelPaletteExtractor":  "Pixel Palette Extractor",
    "CreateColorFromRGBNode": "Create Color From RGB",
    "ColorFormatterNode":     "Color to formatted string",
    "ColorPreviewNode":       "Color to image",
    "MixColorsNode":          "Mix colors",
    "ReplaceColorAtNode":     "Replace Color At Index",
}

# Métadonnées de l'extension
__version__     = "0.0.3"
__author__      = "Ranska"
__description__ = "Extension pour gérer les palettes de pixel art dans ComfyUI"

