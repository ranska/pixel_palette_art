# lib/palette/exporters/__init__.py

from .base_exporter import BaseExporter
from .exporter_registry import ExporterRegistry
from .gimp_exporter import GimpExporter
from .hex_exporter import HexExporter
from .rgb_exporter import RGBExporter
from .css_exporter import CSSExporter
from .amiga_exporter import AmigaExporter

# Enregistrer les exporteurs
ExporterRegistry.register("gimp", GimpExporter)
ExporterRegistry.register("hex", HexExporter)
ExporterRegistry.register("rgb", RGBExporter)
ExporterRegistry.register("css", CSSExporter)
ExporterRegistry.register("amiga", AmigaExporter)