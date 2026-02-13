import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from lib.pixel_color import PixelColor

# spec/color_space_behavior_spec.py
from mamba import description, context, it
from expects import expect, equal

with description('PixelColor mixing behavior'):
    with context('when using different color spaces'):
        with it('change color_space depend on value'):
            color = PixelColor(1.0, 0.0, 0.0)

            expect(color.color_space).to(equal("rgb"))
            with color.using_color_space("hsl"):
                expect(color.color_space).to(equal("hsl"))

            expect(color.color_space).to(equal("rgb"))
            #
            with color.using_color_space("rgb"):
                expect(color.color_space).to(equal("rgb"))
