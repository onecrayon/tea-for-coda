'''Wraps the currently selected text in a tag of the user's choice'''

from Foundation import *
from AppKit import *
from PyObjCTools import AppHelper
import objc

class TEAWrapSelectionInTag(NSObject):
    customSheet = objc.IBOutlet()
    
    prefix = objc.IBOutlet()
    suffix = objc.IBOutlet()
    default = objc.IBOutlet()
    closetag = objc.IBOutlet()
    
    def act(self, controller, bundle):
        # Store the controller and textview for later reference
        self.controller = controller
        self.textview = controller.focusedTextView_(self)
        # Load the sheet
        if not self.customSheet:
            # We have to load from the bundle because this class isn't
            # recognized as belonging to the TEAforCoda bundle
            bundle.loadNibFile_externalNameTable_withZone_(
                'TEAMirroredTagEntry',
                NSDictionary.dictionaryWithObject_forKey_(self, NSNibOwner),
                None
            )
            # NSBundle.loadNibNamed_owner_('TEAMirroredTagEntry', self)
        
        NSApp.beginSheet_modalForWindow_modalDelegate_didEndSelector_contextInfo_(
            self.customSheet,
            self.textview.window(),
            self,
            'didEndSheet:returnCode:contextInfo:',
            None
        )
    
    @objc.IBAction
    def doSubmitSheet_(self, sender):
        NSApp.endSheet_returnCode_(self.customSheet, 1)
    
    @objc.IBAction
    def cancel_(self, sender):
        NSApp.endSheet_returnCode_(self.customSheet, 0)
    
    @AppHelper.endSheetMethod
    def didEndSheet_returnCode_contextInfo_(self, sheet, code, info):
        sheet.orderOut_(self)
