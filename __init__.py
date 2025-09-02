# __init__.py (racine de votre extension)
"""
Extension ComfyUI pour les palettes de pixel art
"""

from .nodes import GimpPaletteLoaderNode, PaletteFormatterNode, PixelPaletteExtractorNode, CreateColorFromRGBNode, ColorFormatterNode, ColorPreviewNode, MixColorsNode
# from .nodes.palette.replace_color_at_node import ReplaceColorAtNode
# Import will be done in NODE_CLASS_MAPPINGS
#  from . import PixelPaletteExtractor

# Configuration ComfyUI
import importlib.util
import os

# Import ReplaceColorAtNode using absolute path
ReplaceColorAtNode = None
node_path = os.path.join(os.path.dirname(__file__), "nodes", "palette", "replace_color_at_node.py")
try:
    spec = importlib.util.spec_from_file_location("replace_color_at_node", node_path)
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

