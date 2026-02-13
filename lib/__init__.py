# lib/__init__.py
"""
Module lib pour la gestion des palettes de pixel art
Contient toute la logique métier des palettes de couleurs
"""

from .pixel_palette import PixelPalette
from .pixel_color   import PixelColor
from . import parsers  # Import the parsers module
from . import palette  # Import the palette module

__all__ = ['PixelPalette', 'PixelColor', 'parsers', 'palette']
__version__ = '1.0.0'
