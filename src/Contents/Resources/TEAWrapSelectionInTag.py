'''Wraps the currently selected text in a tag of the user's choice'''

from Foundation import *
from AppKit import *
from PyObjCTools import AppHelper
import objc

class TEAWrapSelectionInTag(NSWindowController):
    prefix = objc.IBOutlet()
    suffix = objc.IBOutlet()
    default = objc.IBOutlet()
    closetag = objc.IBOutlet()
    
    @objc.IBAction
    def doSubmitSheet_(self, sender):
        NSApp.endSheet_returnCode_(self.customSheet, 1)
    
    @objc.IBAction
    def cancel_(self, sender):
        NSApp.endSheet_returnCode_(self.customSheet, 0)
    
    @AppHelper.endSheetMethod
    def didEndSheet_returnCode_contextInfo_(self, sheet, code, info):
        sheet.orderOut_(self)
    
    def act(self, controller):
        NSLog('Hello world!')
        pass
