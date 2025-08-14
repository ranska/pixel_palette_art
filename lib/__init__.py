# lib/__init__.py
"""
Module lib pour la gestion des palettes de pixel art
Contient toute la logique métier des palettes de couleurs
"""

from .pixel_palette import PixelPalette
from .pixel_color   import PixelColor

__all__ = ['PixelPalette', 'PixelColor']
__version__ = '1.0.0'
