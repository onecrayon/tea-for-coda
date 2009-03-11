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

def load_action(target, search_path):
    '''
    Imports target TEA action file and returns it as a module
    (TEA modules are likely not, by default, in the system path)
    
    Usage: wrap_selection_in_tag = load_action('wrap_selection_in_tag')
    '''
    try:
        # Is the action already loaded?
        module = sys.modules[target]
    except (KeyError, ImportError):
        # Find the action (easiest way to set up the vars we need)
        file, pathname, description = imp.find_module(target, search_path)
        if file is None:
            # Action doesn't exist
            return None
        # File exists, load the action
        module = imp.load_module(
            target, file, pathname, description
        )
    return module

def actions_from_dir(dir, preexisting=[]):
    '''
    Walks through the directory dir looking for Python files; returns
    an array filled with tuples in the format (dir_path, parent_dir, action)
    
    If a preexisting array is passed in, actions are not duplicated
    '''
    pass