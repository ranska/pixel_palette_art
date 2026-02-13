# lib/palette/exporters/base_exporter.py

from abc import ABC, abstractmethod
from typing import List
from ...pixel_color import PixelColor

class BaseExporter(ABC):
    """Classe de base pour les exporteurs de palettes."""

    @abstractmethod
    def export(self, colors: List[PixelColor], **kwargs) -> str:
        """Exporte la liste des couleurs dans le format approprié."""
        pass