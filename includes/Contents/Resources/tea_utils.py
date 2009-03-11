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

def load_action(parent, target):
    '''
    Imports target TEA action file and returns it as a module
    (TEA modules are likely not, by default, in the system path)
    
    Usage: wrap_selection_in_tag = load_action('wrap_selection_in_tag')
    '''
    user_modules, default_modules = default_locations()
    try:
        # Is the action already loaded?
        module = sys.modules[target]
    except (KeyError, ImportError):
        # Find the action (easiest way to set up the vars we need)
        file, pathname, description = imp.find_module(
            target, [user_modules + parent, default_modules + parent]
        )
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
    an array filled with tuples in the format (parent_dir, action)
    
    If a preexisting array is passed in, actions are not duplicated
    '''
    if not os.path.exists(dir):
        return preexisting
    for root, dirs, filenames in os.walk(dir):
        if root is not dir:
            parent_dir = os.path.basename(os.path.dirname(root)) \
                         if root[-1:] == '/' else os.path.basename(root)
        else:
            parent_dir = None
        
        for file in filenames:
            if file[-3:] == '.py':
                action = file[:-3]
                if (parent_dir, action) not in preexisting:
                    preexisting.append((parent_dir, action))
    return preexisting
