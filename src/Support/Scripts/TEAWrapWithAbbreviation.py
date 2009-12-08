'''
Class for wrapping text with ZenCoding's abbreviations
@author: Sergey Chikuyonok (serge.che@gmail.com)
'''

import re

from Foundation import *
from AppKit import *
from PyObjCTools import AppHelper
import objc

import TEASheetLoader
import tea_actions as tea

from zencoding import settings_loader
from zencoding import zen_core as zen
from zencoding import html_matcher as html_matcher

class TEAWrapWithAbbreviation(TEASheetLoader.TEASheetLoader):
    abbr = objc.IBOutlet()
    
    def act(self, controller, bundle, options):
        super(TEAWrapWithAbbreviation, self).loadNib_forController_inBundle_('TEAEnterAbbreviation', controller, bundle)
        
    @AppHelper.endSheetMethod
    def sheetDidEnd_returnCode_contextInfo_(self, sheet, code, info):
        if code == 1:
            self.wrap(self.context, self.abbr.stringValue())
        sheet.orderOut_(self)
        
    def safe_str(self, text):
        """
        Creates safe string representation to deal with Python's encoding issues
        """
        return text.encode('utf-8')
    
    def wrap(self, context, abbr, profile_name='xhtml'):
        # Set up the config variables
        zen_settings = settings_loader.load_settings()
        zen.update_settings(zen_settings)
        zen.newline = self.safe_str(tea.get_line_ending(context))
        zen_settings['variables']['indentation'] = self.safe_str(tea.get_indentation_string(context))
        
        # This allows us to use smart incrementing tab stops in zen snippets
        point_ix = [0]
        def place_ins_point(text):
            if not point_ix[0]:
                point_ix[0] += 1
                return '$0'
            else:
                return ''
        zen.insertion_point = place_ins_point
        
        text, rng = tea.selection_and_range(context)
        if not text:
            # no selection, find matching tag
            content = context.string()
            start, end = html_matcher.match(content, rng.location)
            if start is None:
                # nothing to wrap
                return False
            
            def is_space(char):
                return char.isspace() or char in r'\n\r'
            
            # narrow down selection until first non-space character
            while start < end:
                if not is_space(content[start]):
                    break
                start += 1
            
            while end > start:
                end -= 1
                if not is_space(content[end]):
                    end += 1
                    break
            
            rng = tea.new_range(start, end - start)
            text = tea.get_selection(context, rng)
            
        # NEED A WAY TO DETECT DOCUMENT TYPE
        doc_type = 'html'
        
        text = self.unindent(context, text)
        
        # Damn Python's encodings! Have to convert string to ascii before wrapping 
        # and then back to utf-8
        result = zen.wrap_with_abbreviation(self.safe_str(abbr), self.safe_str(text), doc_type, profile_name)
        result = unicode(result, 'utf-8')
        
        result = tea.indent_snippet(context, result, rng)
        
        cursor_loc = result.find('$0')
        if cursor_loc != -1:
            select_range = tea.new_range(cursor_loc + rng.location, 0)
            snippet = result.replace('$0', '')
            tea.insert_text_and_select(context, snippet, rng, select_range)
        else:
            tea.insert_text(context, snippet, rng)
        
    
    def get_current_line_padding(self, context):
        """
        Returns padding of current editor's line
        @return str
        """
        line, r = tea.get_line(context)
        m = re.match(r'^(\s+)', self.safe_str(line))
        return m and m.group(0) or ''
    
    def unindent(self, context, text):
        """
        Unindent content, thus preparing text for tag wrapping
        @param text: str
        @return str
        """
        pad = self.get_current_line_padding(context)
        lines = zen.split_by_lines(text)
        
        for i,line in enumerate(lines):
            if line.find(pad) == 0:
                lines[i] = line[len(pad):]
        
        return zen.get_newline().join(lines)