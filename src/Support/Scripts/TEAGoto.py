'''
Attempts to go to (select) a location in the document
'''

import re

import tea_actions as tea

def act(controller, bundle, options):
    '''
    Required action method
    
    target dictates what we're looking for:
    - text
    - if unspecified, simply selects the source
    
    source dictates how to gather the string to search for:
    - word (word under the caret)
    - line (line under the caret)
    - if unspecified, defaults to selection
    
    Setting trim=True will cause the source to be trimmed
    
    Setting discard_indent=True will cause leading whitespace
    to be trimmed (unnecessary unless trim=True)
    
    search_string will set the string to search for if target is text or zone
    - $SELECTED_TEXT will be replaced with the source text
    
    Setting regex=True will cause search_string to be evaluated as regex
    '''
    context = tea.get_context(controller)
    
    target = tea.get_option(options, 'target')
    source = tea.get_option(options, 'source')
    trim = tea.get_option(options, 'trim', False)
    discard_indent = tea.get_option(options, 'discard_indent', False)
    search_string = tea.get_option(options, 'search_string')
    regex = tea.get_option(options, 'regex', False)
    
    range = tea.get_range(context)
    if source == 'word':
        text, range = tea.get_word(context, range)
    elif source == 'line':
        text, range = tea.get_line(context)
    elif range.length > 0:
        text = tea.get_selection(context, range)
    
    # Trim the source
    if trim:
        if discard_indent:
            trimmed = tea.trim(context, text, False, preserve_linebreaks=False)
        else:
            trimmed = tea.trim(context, text, False, 'end',
                               preserve_linebreaks=False)
        
        start = text.find(trimmed)
        if start != -1:
            start = range.location + start
        length = len(trimmed)
        if source == 'line' and trimmed[-1:] in ['\r\n', '\r', '\n']:
            # We don't want the linebreak if we're trimming
            length = length - 1
        range = tea.new_range(start, length)
        text = trimmed
    
    if target is not None and text:
        if search_string is not None:
            search = search_string.replace('$SELECTED_TEXT', text)
        else:
            search = text
        # Find the start and end points of the substring
        start = end = None
        if regex:
            match = re.search(r'(' + search + r')', context.string())
            if match:
                # Get the start and end points
                start, end = match.span(1)
        else:
            start = context.string().find(search)
            if start != -1:
                end = start + len(search)
            else:
                start = None
        # Construct the new target range
        if start is not None and end is not None:
            range = tea.new_range(start, end - start)
    
    # Set the new range
    tea.set_selected_range(context, range)
