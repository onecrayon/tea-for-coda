'''Inserts a snippet, including simple cursor positioning'''

import tea_actions as tea

def act(controller, bundle, options):
    context = tea.get_context(controller)
    
    snippet = tea.get_option(options, 'snippet', '')
    maintain_selection = tea.get_option(options, 'maintain_selection', False)
    
    text, range = tea.selection_and_range(context)
    
    snippet = tea.indent_snippet(context, snippet, range)
    
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
        tea.insert_text_and_select(context, snippet, range, select_range)
    else:
        tea.insert_text(context, snippet, range)
