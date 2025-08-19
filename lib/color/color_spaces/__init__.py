# lib/color/color_spaces/__init__.py
"""
Initialisation automatique des espaces colorimétriques
"""
from .rgb.rgb_mixer import RGBMixer
#  from .rgb import RGBExporter, RGBMixer
#  from .hsl import HSLExporter, HSLMixer
#  from .cmyk import CMYKExporter  # Pas de mixer pour CMYK

# lib/color/pixel_color.py
from ..color_space_context import ColorSpaceContext
from ..color_space_registry import ColorSpaceRegistry
# Enregistrement automatique au chargement du module

ColorSpaceRegistry.register('rgb', mixer_class = RGBMixer)
#  ColorSpaceRegistry.register('rgb', RGBExporter, RGBMixer)
#  ColorSpaceRegistry.register('hsl', HSLExporter, HSLMixer)
#  ColorSpaceRegistry.register('cmyk', CMYKExporter)  # Pas de mixer

