
# spec/rgb_mixer_spec.py

# NOTE: we test here pixel color using a mix

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from lib.color.color_spaces.rgb.rgb_exporter import RGBExporter
from lib.pixel_color import PixelColor
#
from mamba import description, context, it
from expects import expect, equal


with description('PixelColor') as self:
    #
    #
    with context('with default color space'):
        with it('mix as rgb'):
            color_a = PixelColor(255, 0, 0, "red")
            color_b = PixelColor(0, 255, 0, "green")

            color_a.mix_with(color_b, 0.5)
            expect(color_a.r).to(equal(128))
            expect(color_a.g).to(equal(128))
            expect(color_a.b).to(equal(0))

        with it('mix as rgb with default value 0.5'):
            color_a = PixelColor(255, 0, 0, "red")
            color_b = PixelColor(0, 255, 0, "green")

            color_a.mix_with(color_b)
            expect(color_a.r).to(equal(128))
            expect(color_a.g).to(equal(128))
            expect(color_a.b).to(equal(0))


    with context('with default color space'):
        print("TODO: test with 2nd color_space like hsl")
