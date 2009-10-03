'''Wraps the currently selected text in a tag of the user's choice'''

import re

from Foundation import *
from PyObjCTools import AppHelper
import objc

import TEASheetLoader

class TEAWrapSelectionInTag(TEASheetLoader.TEASheetLoader):
    prefix = objc.IBOutlet()
    suffix = objc.IBOutlet()
    closetag = objc.IBOutlet()
    
    def act(self, controller, bundle):
        # Pretty standard sheet, so we just have to call the parent
        super(TEAWrapSelectionInTag, self).actInController_forBundle_withNib_(controller, bundle, 'TEAMirroredTagEntry')
        self.prefix.setStringValue_('p')
        self.suffix.setStringValue_('/p')
    
    @AppHelper.endSheetMethod
    def sheetDidEnd_returnCode_contextInfo_(self, sheet, code, info):
        if code == 1:
            current = self.textview.selectedText()
            if current == None:
                current = ''
            range = self.textview.selectedRange()
            # DO PARSING OF ZEN-STYLE STUFF HERE
            replacement = '<' + self.prefix.stringValue() + '>' + current + \
                          '<' + self.suffix.stringValue() + '>'
            self.textview.replaceCharactersInRange_withString_(range, replacement)
        
        sheet.orderOut_(self)
    
    @objc.IBAction
    def customActionsHelp_(self, sender):
        '''Opens URL with help info for custom user actions'''
        url = 'http://onecrayon.com/tea/coda/'
        NSWorkspace.sharedWorkspace().openURL_(NSURL.URLWithString_(url))
    
    def controlTextDidChange_(self, notification):
        self.suffix.setStringValue_(re.sub(r'^([a-zA-Z:-]+).*$', r'/\1', self.prefix.stringValue()))
