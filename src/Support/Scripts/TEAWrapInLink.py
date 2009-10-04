'''Wraps the currently selected text in a tag of the user's choice'''

import subprocess

from Foundation import *

from persistent_re import *
import tea_actions as tea

def act(controller, bundle, options):
    # Grab the context
    context = tea.get_context(controller)
    
    # Setup the options
    fallback = tea.get_option(options, 'fallback', '')
    snippet = tea.get_option(options, 'snippet', '$URL')
    
    # Get the clipboard contents, parse for a URL
    process = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
    clipboard, error = process.communicate(None)
    # Construct the default link
    url = format_hyperlink(clipboard, fallback)
    
    # Grab the selected text and range
    text, range = tea.selection_and_range(context)
    
    # Parse the snippet for $SELECTED_TEXT placeholder
    sel_loc = snippet.find('$SELECTED_TEXT')
    if sel_loc != -1:
        replace_text = True
        prefix = snippet[0:sel_loc]
        suffix = snippet[sel_loc+14:]
    else:
        replace_text = False
        prefix = snippet
        suffix = ''
    
    prefix = prefix.replace('$URL', url)
    suffix = suffix.replace('$URL', url)
    
    if replace_text:
        replacement = prefix + text + suffix
    else:
        replacement = prefix
    
    url_loc = replacement.find(url)
    if url_loc == -1:
        url_loc = len(replacement)
        url_len = 0
    else:
        url_len = len(url)
    newrange = tea.new_range(url_loc + range.location, url_len)
    
    tea.insert_text_and_select(context, replacement, range, newrange)

def format_hyperlink(text, fallback=''):
    gre = persistent_re()
    if gre.match(r'(mailto:)?(.+?@.+\..+)$', text):
        # Email; ensure it has a mailto prefix
        return 'mailto:' + gre.last.group(2)
    elif gre.search(r'http://(?:www\.)?(amazon\.(?:com|co\.uk|co\.jp|ca|fr|de))'\
                    r'/.+?/([A-Z0-9]{10})/[-a-zA-Z0-9_./%?=&]+', text):
        # Amazon URL; rewrite it with short version
        return 'http://' + gre.last.group(1) + '/dp/' + gre.last.group(2)
    elif gre.match(r'[a-zA-Z][a-zA-Z0-9.+-]+?://.*$', text):
        # Unknown prefix
        return tea.tea.encode_ampersands(text)
    elif gre.match(r'.*\.(com|uk|net|org|info)(/.*)?$', text):
        # Recognizable URL without http:// prefix
        return 'http://' + tea.encode_ampersands(text)
    elif gre.match(r'\S+$', text):
        # No space characters, so could be a URL; toss 'er in there
        return tea.encode_ampersands(text)
    else:
        # Nothing that remotely looks URL-ish; give them the fallback
        return fallback
