'''Runs zen coding on the word surrounding the cursor'''

from Foundation import *

import tea_actions as tea
from zencoding import zen_core, settings_loader
from zencoding.zen_settings import zen_settings
from zencoding import html_matcher as html_matcher

def act(controller, bundle, options):
    context = tea.get_context(controller)
    
    # Get the options
    alpha_numeric = tea.get_option(options, 'alpha_numeric', True)
    extra_characters = tea.get_option(options, 'extra_characters', '_-')
    bidirectional = tea.get_option(options, 'bidirectional', True)
    snippet = tea.get_option(options, 'snippet', '<$SELECTED_TEXT>$0</$WORD>')
    mode = tea.get_option(options, 'mode', '')
    
    # Fetch the word
    range = context.selectedRange()
    word, new_range = tea.get_word_or_selection(context, range, alpha_numeric,
                                                extra_characters, bidirectional)
    if word == '':
        # No word, so nothing further to do
        return False
    # If we're using $WORD, make sure the word is just a word
    if snippet.find('$WORD') >= 0:
        fullword = word
        word = tea.parse_word(word)
        if word is None:
            word = ''
    else:
        fullword = word
    
    # Process that sucker!
    if mode == 'zen' and fullword.find(' ') < 0:
        # Explicitly load zen settings
        zen_settings = settings_loader.load_settings()
        zen_core.update_settings(zen_settings)
        
        # Set up the config variables
        zen_core.newline = tea.get_line_ending(context)
        zen_settings['variables']['indentation'] = tea.get_indentation_string(context)
        
        # This allows us to use smart incrementing tab stops in zen snippets
        point_ix = [0]
        def place_ins_point(text):
            if not point_ix[0]:
                point_ix[0] += 1
                return '$0'
            else:
                return ''
            
        zen_core.insertion_point = place_ins_point
        
        # Determine doctype as best we can based on file extension
        doc_type = 'html'
        css_exts = ['css', 'less']
        xsl_exts = ['xsl', 'xslt']
        path = context.path()
        if path is not None:
            pos = path.rfind('.')
            if pos != -1:
                pos += 1
                ext = path[pos:]
                if ext in css_exts:
                    doc_type = 'css'
                elif ext in xsl_exts:
                    doc_type = 'xsl'
        # No luck with the extension; check for inline style tags
        if doc_type == 'html':
            range = tea.get_range(context)
            cursor = range.location + range.length
            content = context.string()
            start, end = html_matcher.match(content, cursor)
            tag = html_matcher.last_match['opening_tag']
            if tag is not None:
                tag = tag.name
                if tag == 'style':
                    doc_type = 'css'
        
        # Prepare the snippet
        snippet = zen_core.expand_abbreviation(fullword, doc_type, 'xhtml')
    elif mode == 'zen' and tea.is_selfclosing(word):
        # Self-closing, so construct the snippet from scratch
        snippet = '<' + fullword
        if fullword == word and not fullword in ['br', 'hr']:
            snippet += ' $0 />'
        else:
            snippet += ' />$0'
    # Indent the snippet
    snippet = tea.indent_snippet(context, snippet, new_range)
    snippet = tea.clean_line_endings(context, snippet)
    # Special replacement in case we're using $WORD
    snippet = snippet.replace('$WORD', word)
    snippet = snippet.replace('$SELECTED_TEXT', fullword)
    cursor_loc = snippet.find('$0')
    if cursor_loc != -1:
        select_range = tea.new_range(cursor_loc + new_range.location, 0)
        snippet = snippet.replace('$0', '')
        tea.insert_text_and_select(context, snippet, new_range, select_range)
    else:
        tea.insert_text(context, snippet, new_range)
