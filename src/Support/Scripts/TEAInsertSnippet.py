'''Inserts a snippet, including simple cursor positioning'''

import tea_actions as tea

def act(controller, bundle, options):
    textview = controller.focusedTextView_(None)
    
    snippet = tea.get_option(options, 'snippet', '')
    maintain_selection = tea.get_option(options, 'maintain_selection', False)
    
    text, range = tea.selection_and_range(textview)
    
    snippet = tea.indent_snippet(textview, snippet, range)
    
    # Set up target selection
    sel_loc = snippet.find('$SELECTED_TEXT')
    cursor_loc = snippet.find('$0')
    if maintain_selection:
        select_range = tea.new_range(sel_loc + range.location, range.length)
    elif cursor_loc != -1:
        select_range = tea.new_range(snippet.find('$0') + range.location, 0)
    else:
        select_range = None
    
    snippet = snippet.replace('$SELECTED_TEXT', text)
    snippet = snippet.replace('$0', '')
    if select_range is not None:
        tea.insert_text_and_select(textview, snippet, range, select_range)
    else:
        tea.insert_text(textview, snippet, range)
