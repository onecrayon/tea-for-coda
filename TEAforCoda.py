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
        setup_actions()
        
        # Add the Resources folder to the path
        sys.path.append(thisBundle.bundlePath() + '/Contents/Resources/')
        
        return self
    
    def name(self):
        '''Required method; returns the name of the plugin'''
        return 'TEA for Coda'
    
    def act(self, caller):
        '''Runs the selected action'''
        pass
