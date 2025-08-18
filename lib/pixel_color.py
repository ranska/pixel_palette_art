
# lib/pixel_palette.py
import re
from typing import List, Tuple, Optional, Dict, Any
from dataclasses import dataclass
from pathlib import Path
#
from .color import mix_strategy
from .color.color_spaces.rgb.rgb_exporter import RGBExporter
from .color.color_space_context import ColorSpaceContext


@dataclass
class PixelColor:
    """Représente une couleur avec ses métadonnées"""
    r:     int
    g:     int
    b:     int
    name:  str = ""
    #
    color_space:  str = "rgb"

    def __post_init__(self):
        # Validation des valeurs RGB
        self.r         = max(0, min(255, int(self.r)))
        self.g         = max(0, min(255, int(self.g)))
        self.b         = max(0, min(255, int(self.b)))
        self._exporter = None


    @property
    def exporter(self):
        if self._exporter is None:
            self._exporter = RGBExporter(self)  # <- self est une référence
        return self._exporter

    @property
    def hex(self) -> str:
        """Retourne la couleur en hexadécimal"""
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"

    @property
    def rgb_tuple(self) -> Tuple[int, int, int]:
        """Retourne un tuple RGB"""
        return (self.r, self.g, self.b)

    @property
    def rgb_normalized(self) -> Tuple[float, float, float]:
        """Retourne RGB normalisé (0.0-1.0)"""
        return (self.r / 255.0, self.g / 255.0, self.b / 255.0)

    def distance_to(self, other: 'Color') -> float:
        """Distance euclidienne entre deux couleurs"""
        return ((self.r - other.r)**2 + (self.g - other.g)**2 + (self.b - other.b)**2) ** 0.5

    def __str__(self):
        return f"{self.hex} ({self.name})" if self.name else self.hex

    def to_hex(self):
        return "#{:02X}{:02X}{:02X}".format(self.r, self.g, self.b)

    @staticmethod
    def mixcolor(a, b, ratio, strategy):
        strategy = strategy.upper()
        if strategy not in mix_strategy.STRATEGIES:
            raise ValueError(f"Stratégie inconnue {strategy}")

        method_name = f"strategy_{strategy.lower()}"
        method      = getattr(mix_strategy, method_name)

        return PixelColor(*method(a, b, ratio))

    #
    #
    def using_color_space(self, new_color_space):
        return ColorSpaceContext(self, new_color_space)
