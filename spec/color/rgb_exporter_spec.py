# spec/pixel_palette_spec.py
from mamba import description, context, it, before
from expects import expect, be_empty, have_length, equal, be_true, be_false, contain, start_with, end_with, expect, equal, be_above_or_equal, be_below_or_equal
import sys
import os

# Ajout du chemin parent pour importer la lib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from lib.pixel_color import PixelColor



#
#  with description('PixelColor') as self:


