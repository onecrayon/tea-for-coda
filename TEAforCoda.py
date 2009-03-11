'''
Textmate Emulation Actions for Coda

A collection of Python scripts that enable useful actions
from Textmate into Coda
'''

from Foundation import *
import objc

from tea_utils import *

NSObject = objc.lookUpClass('NSObject')

class TEAforCoda(NSObject):
    '''
    Initializes the menu items and is responsible for directing
    actions to the appropriate Python script
    '''
    
    def initWithPlugInController_bundle_(self, inController, thisBundle):
        '''Required method; run when the plugin is loaded'''
        self = super(TEAforCoda, self).init()
        if self is None: return None
        
        # Set object's internal variables
        self.controller = inController
        # Setup the menu items
        this.setup_actions();
        
        # Add the Resources folder to the path
        sys.path.append(thisBundle.bundlePath() + '/Contents/Resources/')
        
        return self
    
    def name(self):
        '''Required method; returns the name of the plugin'''
        return 'TEA for Coda'
    
    # Needs trailing underscore for Obj-C to use @selector() on it
    def act_(self, target):
        '''Runs the selected action's act() method'''
        target_module = load_action(target)
        if target_module is None:
            # Couldn't find the module, log the error
            NSLog('TEA: Could not find the module ' + target)
            return False
        target_module.act(self.controller)
    
    def setup_actions(self):
        '''
        Searches through standard folders for actions and populates the
        menus with them using default or predefined shortcuts
        '''
        user_modules, default_modules = default_locations()
        # Walk through the directories and setup the menu items here
        actions = actions_from_dir(user_modules)
        actions = actions_from_dir(default_modules, actions)
        for submenu, action in actions:
            title = action.replace('_', ' ').title()
            self.controller.registerActionWithTitle_underSubmenuWithTitle_target_selector_representedObject_keyEquivalent_pluginName_(
                title,
                submenu,
                self,
                'act:',
                [submenu, action],
                # TODO: fill in shortcut based on preferences
                '',
                title
            )
