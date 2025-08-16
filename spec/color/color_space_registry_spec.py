# spec/color_space_registry_spec.py

from mamba import description, context, it
from expects import expect, equal, contain, raise_error, be_none
from unittest.mock import Mock

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from lib.color.color_space_registry import ColorSpaceRegistry


with description('ColorSpaceRegistry'):
    
    def before_each(self):
        # Clean registry before each test
        ColorSpaceRegistry._spaces = {}
    
    with context('when registering color spaces'):
        
        with it('registers a space with exporter only'):
            mock_exporter = Mock()
            
            ColorSpaceRegistry.register('rgb', mock_exporter)
            
            expect(ColorSpaceRegistry.available_spaces()).to(contain('rgb'))
        
        with it('registers a space with exporter and mixer'):
            mock_exporter = Mock()
            mock_mixer = Mock()
            
            ColorSpaceRegistry.register('hsl', mock_exporter, mock_mixer)
            
            expect(ColorSpaceRegistry.available_spaces()).to(contain('hsl'))
        
        with it('normalizes space names to lowercase'):
            mock_exporter = Mock()
            
            ColorSpaceRegistry.register('RGB', mock_exporter)
            
            expect(ColorSpaceRegistry.available_spaces()).to(contain('rgb'))
    
    with context('when getting exporter classes'):
        
        with it('returns the registered exporter class'):
            mock_exporter = Mock()
            ColorSpaceRegistry.register('rgb', mock_exporter)
            
            result = ColorSpaceRegistry.get_exporter_class('rgb')
            
            expect(result).to(equal(mock_exporter))
        
        with it('is case insensitive'):
            mock_exporter = Mock()
            ColorSpaceRegistry.register('rgb', mock_exporter)
            
            result = ColorSpaceRegistry.get_exporter_class('RGB')
            
            expect(result).to(equal(mock_exporter))
        
        # TODO: fix it
        #  with it('raises error for unknown space'):
            #  expect(lambda: ColorSpaceRegistry.get_exporter_class('unknown')).to(
                #  raise_error(ValueError, 'Espace colorimétrique inconnu: unknown')
            #  )
    
    with context('when getting mixer classes'):
        
        with it('returns the registered mixer class'):
            mock_exporter = Mock()
            mock_mixer = Mock()
            ColorSpaceRegistry.register('hsl', mock_exporter, mock_mixer)
            
            result = ColorSpaceRegistry.get_mixer_class('hsl')
            
            expect(result).to(equal(mock_mixer))
        
        with it('raises error when no mixer is available'):
            mock_exporter = Mock()
            ColorSpaceRegistry.register('rgb', mock_exporter)
            
            expect(lambda: ColorSpaceRegistry.get_mixer_class('rgb')).to(
                raise_error(ValueError, 'Pas de mixer disponible pour: rgb')
            )
        
        with it('raises error for unknown space'):
            expect(lambda: ColorSpaceRegistry.get_mixer_class('unknown')).to(
                raise_error(ValueError, 'Espace colorimétrique inconnu: unknown')
            )
    
    with context('when getting space info'):
        
        with it('returns complete space information'):
            mock_exporter = Mock()
            mock_mixer = Mock()
            ColorSpaceRegistry.register('hsl', mock_exporter, mock_mixer)
            
            result = ColorSpaceRegistry.get_space_info('hsl')
            
            expect(result).to(equal({
                'exporter': mock_exporter,
                'mixer': mock_mixer
            }))
        
        with it('returns space info with None mixer'):
            mock_exporter = Mock()
            ColorSpaceRegistry.register('rgb', mock_exporter)
            
            result = ColorSpaceRegistry.get_space_info('rgb')
            
            expect(result).to(equal({
                'exporter': mock_exporter,
                'mixer': None
            }))
        
        with it('raises error for unknown space'):
            expect(lambda: ColorSpaceRegistry.get_space_info('unknown')).to(
                raise_error(ValueError, 'Espace colorimétrique inconnu: unknown')
            )
        
        # TODO: fix it
        #  with it('returns a copy of the data'):
            #  mock_exporter = Mock()
            #  ColorSpaceRegistry.register('rgb', mock_exporter)
            
            #  result = ColorSpaceRegistry.get_space_info('rgb')
            #  result['new_key'] = 'modified'
            
            #  original = ColorSpaceRegistry.get_space_info('rgb')
            #  expect(original).to_not(contain('new_key'))
    
    with context('when listing available spaces'):
        
        with it('returns empty list when no spaces registered'):
            expect(ColorSpaceRegistry.available_spaces()).to(equal([]))
        
        with it('returns all registered space names'):
            mock_exporter = Mock()
            ColorSpaceRegistry.register('rgb', mock_exporter)
            ColorSpaceRegistry.register('hsl', mock_exporter)
            
            result = ColorSpaceRegistry.available_spaces()
            
            expect(result).to(contain('rgb', 'hsl'))
            expect(len(result)).to(equal(2))
