# lib/palette/exporter_context.py

from typing import TYPE_CHECKING, Optional, Any

if TYPE_CHECKING:
    from ..pixel_palette import PixelPalette

class PaletteExporter:
    """Context manager pour l'export des palettes, similaire au pattern color.mix"""

    def __init__(self, palette: 'PixelPalette', format_type: str):
        self.palette = palette
        self.format_type = format_type
        self.exporter: Optional[Any] = None

    def __enter__(self):
        from .exporters.exporter_registry import ExporterRegistry
        exporter_class = ExporterRegistry.get_exporter_class(self.format_type)
        self.exporter = exporter_class()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def export(self, **kwargs):
        """Exporte la palette selon le format"""
        if self.exporter is None:
            raise RuntimeError("Context not entered")
        return self.exporter.export(self.palette.colors, **kwargs)

    def export_list(self, **kwargs):
        """Exporte la palette comme liste de strings"""
        if self.exporter is None:
            raise RuntimeError("Context not entered")
        content = self.exporter.export(self.palette.colors, separator="\n", **kwargs)
        return content.split("\n") if content else []

    def export_tuples(self):
        """Exporte la palette comme liste de tuples RGB"""
        if self.exporter is None:
            raise RuntimeError("Context not entered")
        if hasattr(self.exporter, 'export_tuples'):
            return self.exporter.export_tuples(self.palette.colors)
        return []