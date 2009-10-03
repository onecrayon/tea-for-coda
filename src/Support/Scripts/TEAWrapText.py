'''Wraps the currently selected text in a tag of the user's choice'''

import re

from Foundation import *
from AppKit import *
from PyObjCTools import AppHelper
import objc

import TEASheetLoader

class TEAWrapText(TEASheetLoader.TEASheetLoader):
    prefix = objc.IBOutlet()
    suffix = objc.IBOutlet()
    
    def act(self, controller, bundle, options):
        # Set up our options
        prefix = options.objectForKey_('prefix')
        suffix = options.objectForKey_('suffix')
        self.query_user = options.objectForKey_('query_user')
        if self.query_user is None:
            self.query_user = True
        self.wrap_lines = options.objectForKey_('wrap_lines')
        if self.wrap_lines is None:
            self.wrap_lines = False
        self.format = options.objectForKey_('format')
        
        if self.query_user:
            if self.format.lower() == 'html':
                super(TEAWrapText, self).loadNib_forController_inBundle_('TEAMirroredTagEntry', controller, bundle)
            else:
                super(TEAWrapText, self).loadNib_forController_inBundle_('TEAPrefixSuffixEntry', controller, bundle)
        else:
            super(TEAWrapText, self).initController_forBundle_(controller, bundle)
        
        if self.prefix is not None and self.prefix.className() == 'NSTextField' and prefix is not None:
            self.prefix.setStringValue_(prefix)
        else:
            self.prefix = prefix if prefix is not None else ''
        if self.suffix is not None and self.suffix.className() == 'NSTextField' and suffix is not None:
            self.suffix.setStringValue_(suffix)
        else:
            self.suffix = suffix if suffix is not None else ''
        # Track the prefix length in case the selection is empty
        self.prefix_length = None
        
        if not self.query_user:
            self.process_text()
    
    def process_text(self):
        # Helper function to do zen-style conversions for tag
        global increment
        increment = 1
        def string_to_tag(string):
            '''
            Parses a string into a tag with id and class attributes
            
            For example, div#stuff.good.things translates into
            `div id="stuff" class="good things"`
            '''
            if string.find('#') > 0 or string.find('.') > 0:
                match = re.search(r'#([a-zA-Z0-9$_-]+)', string)
                if match:
                    id = match.group(1)
                else:
                    id = False
                matches = re.findall(r'\.([a-zA-Z0-9$_-]+)', string)
                classes = ''
                for match in matches:
                    if classes:
                        classes += ' '
                    classes += match
                tag = re.sub(r'^([a-zA-Z_:-]+).*$', r'\1', string)
                if id:
                    tag += ' id="' + id + '"'
                if classes:
                    tag += ' class="' + classes + '"'
                if tag.find('$') != -1:
                    tag = tag.replace('$', str(increment))
                    globals()['increment'] += 1
                return tag
            else:
                return string
        
        # Helper function to do actual wrapping
        def wrap(text, prefix, suffix):
            if self.format.lower() == 'html':
                prefix = string_to_tag(prefix)
                prefix = '<' + prefix + '>'
                suffix = '<' + suffix + '>'
                if self.prefix_length is None:
                    self.prefix_length = len(prefix)
            return prefix + text + suffix
        
        # Grab the prefix and suffix
        if self.prefix.className() == 'NSTextField':
            prefix = self.prefix.stringValue()
        else:
            prefix = self.prefix
        if self.suffix.className() == 'NSTextField':
            suffix = self.suffix.stringValue()
        else:
            suffix = self.suffix
        
        # Grab the selection and selected range
        selection = self.textview.selectedText()
        if selection == None:
            selection = ''
        range = self.textview.selectedRange()
        
        # Set up the lines array based on whether or not we're wrapping lines
        if self.wrap_lines:
            # Split the text into lines, maintaining the linebreaks
            lines = selection.splitlines(True)
            # Compile the regex for quicker action on lots of lines
            parser = re.compile(r'(\s*)(.*?)(\s*(\r|\r\n|\n)|$)')
        else:
            # Use a lines array for ease of coding anyway
            lines = [selection]
        
        # Construct our replacement text
        replacement = ''
        for line in lines:
            if self.wrap_lines:
                content = parser.search(line)
                # Only wrap the line if there's some content
                if content.group(2) != '':
                    text = wrap(content.group(2), prefix, suffix)
                    replacement += content.group(1) + text + content.group(3)
                else:
                    replacement += line
            else:
                # Just wrapping the selection, so no whitespace logic
                replacement += wrap(line, prefix, suffix)
        
        # Insert the new text
        self.textview.beginUndoGrouping()
        self.textview.replaceCharactersInRange_withString_(range, replacement)
        if selection == '' and prefix != '' and suffix != '':
            # No selection, so position cursor inside
            newrange = NSMakeRange(range.location + self.prefix_length, 0)
            self.textview.setSelectedRange_(newrange)
        self.textview.endUndoGrouping()
    
    @AppHelper.endSheetMethod
    def sheetDidEnd_returnCode_contextInfo_(self, sheet, code, info):
        if code == 1:
            self.process_text()
        sheet.orderOut_(self)
    
    @objc.IBAction
    def customActionsHelp_(self, sender):
        '''Opens URL with help info for custom user actions'''
        url = 'http://onecrayon.com/tea/coda/'
        NSWorkspace.sharedWorkspace().openURL_(NSURL.URLWithString_(url))
    
    def controlTextDidChange_(self, notification):
        if self.format.lower() == 'html':
            self.suffix.setStringValue_(re.sub(r'^([a-zA-Z:-]+).*$', r'/\1', self.prefix.stringValue()))
