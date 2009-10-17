'''
Trims the text; what is trimmed depends on what's passed in via XML
'''

import tea_actions as tea

def act(controller, bundle, options):
    '''
    Required action method
    
    input dictates what should be trimmed:
    - None (default): falls back to alternate
    - selection: ignores lines if they exist, just trims selection
    - selected_lines: each line in the selection
    
    alternate dictates what to fall back on
    - None (default): will do nothing if input is blank
    - line: will trim the line the caret is on
    - all_lines: all lines in the document
    
    trim dictates what part of the text should be trimmed:
    - both (default)
    - start
    - end
    
    If respect_indent is True, indent characters (as defined in preferences)
    at the beginning of the line will be left untouched.
    '''
    context = tea.get_context(controller)
    
    input = tea.get_option(options, 'input')
    alternate = tea.get_option(options, 'alternate')
    trim = tea.get_option(options, 'trim', 'both')
    respect_indent = tea.get_option(options, 'respect_indent', False)
    discard_empty = tea.get_option(options, 'discard_empty', False)
    
    # Since input is always a selection of some kind, check if we have one
    range = tea.get_range(context)
    
    if (range.length == 0) or input is None:
        if alternate.lower() == 'line':
            text, range = tea.get_line(context)
            text = tea.trim(context, text, False, trim, respect_indent, True, discard_empty)
        elif alternate.lower() == 'all_lines':
            range = tea.new_range(0, context.string().length())
            text = tea.get_selection(context, range)
            text = tea.trim(context, text, True, trim, respect_indent, True, discard_empty)
    else:
        if input.lower() == 'selected_lines':
            parse_lines = True
        else:
            parse_lines = False
        text = tea.get_selection(context, range)
        text = tea.trim(context, text, parse_lines, trim, respect_indent, True, discard_empty)
    tea.insert_text(context, text, range)
    new_range = tea.new_range(range.location, len(text))
    tea.set_selected_range(context, new_range)
