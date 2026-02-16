# spec/palette/exporters/exporter_registry_spec.py

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))

from lib.palette.exporters.exporter_registry import ExporterRegistry
from lib.palette.exporters.rgb_exporter import RGBExporter
from lib.palette.exporters.gimp_exporter import GimpExporter
from mamba import description, context, it, before
from expects import expect, equal, be_a, have_length, contain, raise_error


with description('ExporterRegistry') as self:

    with before.each:
        # Sauvegarder l'état et repartir propre
        self._saved = dict(ExporterRegistry._exporters)
        ExporterRegistry.reset()

    with context('reset'):
        with it('vide completement le registre'):
            ExporterRegistry.register('rgb', RGBExporter)
            ExporterRegistry.reset()
            expect(ExporterRegistry.available_formats()).to(have_length(0))

    with context('register et get_exporter_class'):
        with it('enregistre et retrouve un exporter'):
            ExporterRegistry.register('rgb', RGBExporter)
            expect(ExporterRegistry.get_exporter_class('rgb')).to(equal(RGBExporter))

        with it('normalise le nom en minuscules'):
            ExporterRegistry.register('GIMP', GimpExporter)
            expect(ExporterRegistry.get_exporter_class('gimp')).to(equal(GimpExporter))

    with context('get_exporter_class avec format inconnu'):
        with it('leve ValueError'):
            expect(lambda: ExporterRegistry.get_exporter_class('unknown')).to(
                raise_error(ValueError)
            )

    with context('available_formats'):
        with it('retourne la liste des formats enregistres'):
            ExporterRegistry.register('rgb', RGBExporter)
            ExporterRegistry.register('gimp', GimpExporter)
            formats = ExporterRegistry.available_formats()
            expect(formats).to(contain('rgb'))
            expect(formats).to(contain('gimp'))

        with it('retourne une liste vide si rien enregistre'):
            expect(ExporterRegistry.available_formats()).to(have_length(0))

    # Restaurer l'état initial pour ne pas casser les autres specs
    with after.each:
        ExporterRegistry._exporters = self._saved
