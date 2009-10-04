'''Generic class for TEA sheets'''

from Foundation import *
from AppKit import *
from PyObjCTools import AppHelper
import objc

import tea_actions as tea

class TEASheetLoader(NSObject):
    customSheet = objc.IBOutlet()
    
    def initController_forBundle_(self, controller, bundle):
        # Store the controller and context for later reference
        self.controller = controller
        self.context = tea.get_context(controller, self)
    
    def loadNib_forController_inBundle_(self, nibName, controller, bundle):
        self.initController_forBundle_(controller, bundle)
        # Load the sheet
        if not self.customSheet:
            # We have to load from the bundle because this class isn't
            # recognized as belonging to the TEAforCoda bundle
            bundle.loadNibFile_externalNameTable_withZone_(
                nibName,
                NSDictionary.dictionaryWithObject_forKey_(self, NSNibOwner),
                None
            )
        
        NSApp.beginSheet_modalForWindow_modalDelegate_didEndSelector_contextInfo_(
            self.customSheet,
            self.context.window(),
            self,
            'sheetDidEnd:returnCode:contextInfo:',
            None
        )
        # Retain the class to make sure it sticks around for the window events
        self.retain()
    
    @objc.IBAction
    def doSubmitSheet_(self, sender):
        NSApp.endSheet_returnCode_(self.customSheet, 1)
    
    @objc.IBAction
    def cancel_(self, sender):
        NSApp.endSheet_returnCode_(self.customSheet, 0)
    
    def windowWillClose_(self, notification):
        '''Delegate method to auto-release everything'''
        # Unless we retain then self-release, we'll lose the window to the
        # default garbage collector; this delegate method is automatic
        self.autorelease()
