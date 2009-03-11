'''
This module includes common utility functions for working with
TEA actions, such as locating and loading them
'''

import imp
import sys
import os.path

def default_locations():
    user_modules = os.path.expanduser(
        '~/Library/Application Support/Coda/TEA/'
    )
    default_modules = os.path.expanduser(
        '~/Library/Application Support/Coda/Plug-ins/'
        'TEA for Coda.codaplugin/TEA/'
    )
    return user_modules, default_modules
