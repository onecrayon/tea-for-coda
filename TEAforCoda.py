'''
Textmate Emulation Actions for Coda

A collection of Python scripts that enable useful actions
from Textmate into Coda
'''

from Foundation import *
import objc

NSObject = objc.lookUpClass('NSObject')

class TEAforCoda(NSObject):
    '''Docstring here'''
    
    def initWithPlugInController_bundle_(self, inController, yourBundle):
        '''Required method; run when the plugin is loaded'''
        self = super(TEAforCoda, self).init()
        if self is None: return None
        
        # Set object's internal variables
        self.controller = inController
        # TODO: Setup the menu items here
        
        return self
    
    def name(self):
        '''Required method; returns the name of the plugin'''
        return 'TEA for Coda'
