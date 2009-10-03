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

import sys
import os.path

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
        
        self.controller = controller
        self.bundle = bundle
        
        # Loop over the actions and add them to the menus
        for action in actions:
            if 'class' not in action or 'title' not in action:
                NSLog('TEA: module missing either `class` or `title` entries')
                continue
            # Required items
            title = action['title']
            classname = action['class']
            # Set up defaults
            submenu = action['submenu'] if 'submenu' in action else None
            shortcut = action['shortcut'] if 'shortcut' in action else ''
            options = action['options'] if 'options' in action else NSDictionary.dictionary()
            
            rep = NSDictionary.dictionaryWithObjectsAndKeys_(
                classname,
                'classname',
                options,
                'options'
            )
            controller.registerActionWithTitle_underSubmenuWithTitle_target_selector_representedObject_keyEquivalent_pluginName_(
                title,
                submenu,
                self,
                'act:',
                rep,
                shortcut,
                'TEA for Coda'
            )
        
        # Add the Support/Scripts folder to the Python import path
        sys.path.append(os.path.join(bundle.bundlePath(), "Support/Scripts"))
        sys.path.append(os.path.join(bundle.bundlePath(), "Support/Library"))
        
        return self
    
    def name(self):
        '''Required method; returns the name of the plugin'''
        return 'TEA for Coda'
    
    def act_(self, sender):
        '''
        Imports the module, initializes the class, and runs its act() method
        '''
        classname = sender.representedObject().objectForKey_('classname')
        mod = __import__(classname)
        if classname in mod.__dict__:
            target = mod.__dict__[classname].alloc().init()
        else:
            target = mod
        target.act(self.controller, self.bundle, sender.representedObject().objectForKey_('options'))
