# nodes/__init__.py
"""
Nodes pour ComfyUI
Export des nodes disponibles
"""

from .gimp_palette_loader_node     import GimpPaletteLoaderNode
from .palette_formatter_node       import PaletteFormatterNode
from .pixel_palette_extractor_noed import PixelPaletteExtractor

__all__ = [
    'GimpPaletteLoaderNode',
    'PaletteFormatterNode',
    "PixelPaletteExtractorNode",
]
