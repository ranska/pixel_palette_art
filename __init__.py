
"""
Pixel Palette Art - Custom Node pour ComfyUI
Extracteur de palette de couleurs pour images GIF indexées et chargeur de palettes GIMP
"""

from .nodes import NODE_CLASS_MAPPINGS as NODES_MAPPING, NODE_DISPLAY_NAME_MAPPINGS as NODES_DISPLAY
from .gimp_palette_loader import GIMP_NODE_CLASS_MAPPINGS, GIMP_NODE_DISPLAY_NAME_MAPPINGS

# Combiner tous les mappings
NODE_CLASS_MAPPINGS = {}
NODE_CLASS_MAPPINGS.update(NODES_MAPPING)
NODE_CLASS_MAPPINGS.update(GIMP_NODE_CLASS_MAPPINGS)

NODE_DISPLAY_NAME_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS.update(NODES_DISPLAY)
NODE_DISPLAY_NAME_MAPPINGS.update(GIMP_NODE_DISPLAY_NAME_MAPPINGS)

# Export des mappings pour ComfyUI
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

# Informations du module
#  WEB_DIRECTORY = "./web"
