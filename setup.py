# Usage: python setup.py py2app
# Dev:   python setup.py py2app -A
# Built plugin will show up in ./dist directory
# Install in the standard Sugars directory and relaunch Espresso to run

from distutils.core import setup
import py2app

setup(
    name='TEA for Coda',
    plugin = ['TEAforCoda.py'],
    options=dict(py2app=dict(
        extension='.codaplugin',
        semi_standalone = True,
    )),
)