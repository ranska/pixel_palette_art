# __init__.py (racine de votre extension)
"""
Extension ComfyUI pour les palettes de pixel art
"""

from .nodes import (GimpPaletteLoaderNode, PaletteFormatterNode,
                     PixelPaletteExtractorNode, CreateColorFromRGBNode,
                     ColorFormatterNode, ColorPreviewNode, MixColorsNode,
                     ReplaceColorAtNode, SortPaletteNode,
                     GradientBetweenNode, CreateGradientPaletteNode,
                     PaletteViewNode, CopySubsetNode, AppendPaletteNode,
                     InsertPaletteNode, MixPaletteNode)

NODE_CLASS_MAPPINGS = {
    "GimpPaletteLoader":        GimpPaletteLoaderNode,
    "PaletteFormatter":         PaletteFormatterNode,
    "PixelPaletteExtractor":    PixelPaletteExtractorNode,
    "CreateColorFromRGBNode":   CreateColorFromRGBNode,
    "ColorFormatterNode":       ColorFormatterNode,
    "ColorPreviewNode":         ColorPreviewNode,
    "MixColorsNode":            MixColorsNode,
    "ReplaceColorAtNode":       ReplaceColorAtNode,
    "SortPaletteNode":          SortPaletteNode,
    "GradientBetweenNode":      GradientBetweenNode,
    "CreateGradientPaletteNode": CreateGradientPaletteNode,
    "PaletteViewNode":          PaletteViewNode,
    "CopySubsetNode":           CopySubsetNode,
    "AppendPaletteNode":        AppendPaletteNode,
    "InsertPaletteNode":        InsertPaletteNode,
    "MixPaletteNode":           MixPaletteNode,
}

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
    "CopySubsetNode":           "Copy Subset",
    "AppendPaletteNode":        "Append Palette",
    "InsertPaletteNode":        "Insert Palette At Index",
    "MixPaletteNode":           "Mix Palettes",
}

# Métadonnées de l'extension
__version__     = "0.0.3"
__author__      = "Ranska"
__description__ = "Extension pour gérer les palettes de pixel art dans ComfyUI"
