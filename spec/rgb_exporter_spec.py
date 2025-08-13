
# spec/rgb_exporter_spec.py

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from lib.color.rgb_exporter import RGBExporter
from mamba import description, context, it
from expects import expect, equal


class MockPixelColor:
    """Mock de PixelColor pour les specs"""
    def __init__(self, r, g, b, name=""):
        self.r = r
        self.g = g
        self.b = b
        self.name = name


with description('RGBExporter') as self:
    
    #
    # hex
    #
    with context('when exporting to hex formats'):
        with it('exports basic hex format correctly'):
            color = MockPixelColor(255, 128, 0, "Orange")
            exporter = RGBExporter(color)
            result = exporter.to_hex()
            expect(result).to(equal("#FF8000"))
        
        with it('exports hex with alpha correctly'):
            color = MockPixelColor(255, 128, 0, "Orange")
            exporter = RGBExporter(color)
            result = exporter.to_hex_alpha(128)
            expect(result).to(equal("#FF800080"))
        
        with it('uses default alpha when not specified'):
            color = MockPixelColor(255, 128, 0, "Orange")
            exporter = RGBExporter(color)
            result = exporter.to_hex_alpha()
            expect(result).to(equal("#FF8000FF"))
    
    #
    # string rgb
    #
    with context('when exporting to RGB string formats'):
        with it('exports RGB string correctly'):
            color = MockPixelColor(255, 128, 0, "Orange")
            exporter = RGBExporter(color)
            result = exporter.to_rgb_string()
            expect(result).to(equal("rgb(255, 128, 0)"))
        
        with it('exports RGBA string with custom alpha'):
            color = MockPixelColor(255, 128, 0, "Orange")
            exporter = RGBExporter(color)
            result = exporter.to_rgba_string(0.5)
            expect(result).to(equal("rgba(255, 128, 0, 0.5)"))
        
        with it('uses default alpha in RGBA string'):
            color = MockPixelColor(255, 128, 0, "Orange")
            exporter = RGBExporter(color)
            result = exporter.to_rgba_string()
            expect(result).to(equal("rgba(255, 128, 0, 1.0)"))
    
    #
    # python tuple
    #
    with context('when exporting to tuple formats'):
        with it('exports RGB tuple correctly'):
            color = MockPixelColor(255, 128, 0, "Orange")
            exporter = RGBExporter(color)
            result = exporter.to_rgb_tuple()
            expect(result).to(equal((255, 128, 0)))
        
        with it('exports RGBA tuple with custom alpha'):
            color = MockPixelColor(255, 128, 0, "Orange")
            exporter = RGBExporter(color)
            result = exporter.to_rgba_tuple(200)
            expect(result).to(equal((255, 128, 0, 200)))
        
        with it('uses default alpha in RGBA tuple'):
            color = MockPixelColor(255, 128, 0, "Orange")
            exporter = RGBExporter(color)
            result = exporter.to_rgba_tuple()
            expect(result).to(equal((255, 128, 0, 255)))
    
    #
    # HSL
    #
    with context('when exporting to HSL format'):
        with it('converts orange color to HSL correctly'):
            color = MockPixelColor(255, 128, 0, "Orange")
            exporter = RGBExporter(color)
            result = exporter.to_hsl_string()
            expect(result).to(equal("hsl(30, 100%, 50%)"))
        
        with it('converts gray color to HSL correctly'):
            color = MockPixelColor(128, 128, 128, "Gray")
            exporter = RGBExporter(color)
            result = exporter.to_hsl_string()
            expect(result).to(equal("hsl(0, 0%, 50%)"))
    
    #
    # css
    #
    with context('when exporting to CSS format'):
        with it('exports CSS variable correctly'):
            color = MockPixelColor(255, 128, 0, "Orange")
            exporter = RGBExporter(color)
            result = exporter.to_css_var("primary")
            expect(result).to(equal("--primary: #FF8000;"))
        
        with it('handles CSS variable with dashes'):
            color = MockPixelColor(255, 128, 0, "Orange")
            exporter = RGBExporter(color)
            result = exporter.to_css_var("brand-color")
            expect(result).to(equal("--brand-color: #FF8000;"))
    
    #
    # Gimp palette format
    #
    with context('when exporting to GIMP palette format'):
        with it('exports named color correctly'):
            color = MockPixelColor(255, 128, 0, "Orange")
            exporter = RGBExporter(color)
            result = exporter.to_gimp_palette_line()
            expect(result).to(equal("255 128   0\tOrange"))
        
        with it('exports unnamed color with index'):
            color = MockPixelColor(100, 50, 200, "")
            exporter = RGBExporter(color)
            result = exporter.to_gimp_palette_line(3)
            expect(result).to(equal("100  50 200\tColor_3"))
        
        with it('exports unnamed color without index'):
            color = MockPixelColor(100, 50, 200, "")
            exporter = RGBExporter(color)
            result = exporter.to_gimp_palette_line()
            expect(result).to(equal("100  50 200\tUntitled"))
        
        with it('prefers color name over index'):
            color = MockPixelColor(255, 128, 0, "Orange")
            exporter = RGBExporter(color)
            result = exporter.to_gimp_palette_line(5)
            expect(result).to(equal("255 128   0\tOrange"))
