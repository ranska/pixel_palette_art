# __init__.py (racine de votre extension)
"""
Extension ComfyUI pour les palettes de pixel art
"""

from .nodes import GimpPaletteLoaderNode, PaletteFormatterNode, PixelPaletteExtractorNode, CreateColorFromRGBNode, ColorFormatterNode, ColorPreviewNode, MixColorsNode

# Import des nodes palette/ via importlib pour compatibilité ComfyUI
import importlib.util
import os

def _load_palette_node(module_name, class_name):
    """Charge un node depuis nodes/palette/ via importlib"""
    try:
        node_file = os.path.join(os.path.dirname(__file__), "nodes", "palette", f"{module_name}.py")
        spec = importlib.util.spec_from_file_location(module_name, node_file)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return getattr(module, class_name)
    except Exception as e:
        print(f"Warning: Could not import {class_name}: {e}")
    return None

ReplaceColorAtNode = _load_palette_node("replace_color_at_node", "ReplaceColorAtNode")
SortPaletteNode = _load_palette_node("sort_palette_node", "SortPaletteNode")
GradientBetweenNode = _load_palette_node("gradient_between_node", "GradientBetweenNode")
CreateGradientPaletteNode = _load_palette_node("create_gradient_palette_node", "CreateGradientPaletteNode")
PaletteViewNode = _load_palette_node("palette_view_node", "PaletteViewNode")

NODE_CLASS_MAPPINGS = {
    "GimpPaletteLoader":      GimpPaletteLoaderNode,
    "PaletteFormatter":       PaletteFormatterNode,
    "PixelPaletteExtractor":  PixelPaletteExtractorNode,
    "CreateColorFromRGBNode": CreateColorFromRGBNode,
    "ColorFormatterNode":     ColorFormatterNode,
    "ColorPreviewNode":       ColorPreviewNode,
    "MixColorsNode":          MixColorsNode,
}

# Ajout conditionnel des nodes palette/
_palette_nodes = {
    "ReplaceColorAtNode":       ReplaceColorAtNode,
    "SortPaletteNode":          SortPaletteNode,
    "GradientBetweenNode":      GradientBetweenNode,
    "CreateGradientPaletteNode": CreateGradientPaletteNode,
    "PaletteViewNode":          PaletteViewNode,
}
for name, cls in _palette_nodes.items():
    if cls is not None:
        NODE_CLASS_MAPPINGS[name] = cls

NODE_DISPLAY_NAME_MAPPINGS = {
    "GimpPaletteLoader":        "GIMP Palette Loader",
    "PaletteFormatter":         "Palette Formatter",
    "PixelPaletteExtractor":    "Pixel Palette Extractor",
    "CreateColorFromRGBNode":   "Create Color From RGB",
    "ColorFormatterNode":       "Color to formatted string",
    "ColorPreviewNode":         "Color to image",
    "MixColorsNode":            "Mix colors",
    "ReplaceColorAtNode":       "Replace Color At Index",
    "SortPaletteNode":          "Sort Palette",
    "GradientBetweenNode":      "Gradient Between Indices",
    "CreateGradientPaletteNode": "Create Gradient Palette",
    "PaletteViewNode":          "Palette View",
}

# Métadonnées de l'extension
__version__     = "0.0.3"
__author__      = "Ranska"
__description__ = "Extension pour gérer les palettes de pixel art dans ComfyUI"
