'''Runs zen coding on the word surrounding the cursor'''

from Foundation import *

import tea_actions as tea
from zencoding import zen_core
from zencoding.settings import zen_settings

def act(controller, bundle, options):
    textview = controller.focusedTextView_(None)
    
    # Get the options
    alpha_numeric = tea.get_option(options, 'alpha_numeric', True)
    extra_characters = tea.get_option(options, 'extra_characters', '_-')
    bidirectional = tea.get_option(options, 'bidirectional', True)
    snippet = tea.get_option(options, 'snippet', '<$SELECTED_TEXT>$0</$WORD>')
    mode = tea.get_option(options, 'mode', '')
    
    # Fetch the word
    range = textview.selectedRange()
    word, new_range = tea.get_word_or_selection(textview, range, alpha_numeric,
                                                extra_characters, bidirectional)
    if word == '':
        # No word, so nothing further to do
        return
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
        # Set up the config variables
        zen_core.newline = tea.get_line_ending(textview)
        zen_core.insertion_point = '$0'
        zen_core.sub_insertion_point = ''
        zen_settings['indentation'] = tea.get_indentation_string(textview)
        
        # NEED A WAY TO DETECT DOCUMENT TYPE
        doc_type = 'html'
        
        # Prepare the snippet
        snippet = zen_core.expand_abbr(fullword, doc_type)
    elif mode == 'zen' and tea.is_selfclosing(word):
        # Self-closing, so construct the snippet from scratch
        snippet = '<' + fullword
        if fullword == word and not fullword in ['br', 'hr']:
            snippet += ' $0 />'
        else:
            snippet += ' />$0'
    # Indent the snippet
    snippet = tea.indent_snippet(textview, snippet, new_range)
    # Special replacement in case we're using $WORD
    snippet = snippet.replace('$WORD', word)
    snippet = snippet.replace('$SELECTED_TEXT', fullword)
    cursor_loc = snippet.find('$0')
    if cursor_loc != -1:
        select_range = tea.new_range(cursor_loc + new_range.location, 0)
        snippet = snippet.replace('$0', '')
        tea.insert_text_and_select(textview, snippet, new_range, select_range)
    else:
        tea.insert_text(textview, snippet, new_range)
