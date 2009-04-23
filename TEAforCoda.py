'''
Text Editor Actions for Coda

A collection of Python scripts that enable useful actions
from Textmate into Coda

Copyright (c) 2009 Ian Beck

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

from Foundation import *
import objc

NSObject = objc.lookUpClass('NSObject')
CodaPlugIn = objc.protocolNamed('CodaPlugIn')

class TEAforCoda(NSObject, CodaPlugIn):
    '''
    Initializes the menu items and is responsible for directing
    actions to the appropriate class
    '''
    
    def initWithPlugInController_bundle_(self, controller, bundle):
        '''Required method; run when the plugin is loaded'''
        self = super(TEAforCoda, self).init()
        if self is None: return None
        
        defaults = NSUserDefaults.standardUserDefaults()
        # Set up default action set
        defaults.registerDefaults_(NSDictionary.dictionaryWithContentsOfFile_(
            bundle.pathForResource_ofType_('TextActions', 'plist')
        ))
        actions = defaults.arrayForKey_('TEATextActions')
        
        # Loop over the actions and add them to the menus
        for action in actions:
            if 'class' not in action or 'title' not in action:
                NSLog('TEA: module missing either `class` or `title` entries')
                continue
            # Required items
            title = action['title']
            mod = __import__(action['class'])
            target = mod.__dict__(title)
            # Set up defaults
            submenu = action['submenu'] if 'submenu' in action else None
            shortcut = action['shortcut'] if 'shortcut' in action else ''
            self.controller.registerActionWithTitle_underSubmenuWithTitle_target_selector_representedObject_keyEquivalent_pluginName_(
                title,
                submenu,
                target,
                'act:',
                controller,
                shortcut,
                title
            )
        
        return self
    
    def name(self):
        '''Required method; returns the name of the plugin'''
        return 'TEA for Coda'
