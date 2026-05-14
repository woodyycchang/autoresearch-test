"""Parser: turn flat token stream from lexer into a block-level AST.

AST nodes are dicts:
- {'type':'header','level':int,'text':str}
- {'type':'code','lang':str,'text':str}     -- raw, never inline-formatted
- {'type':'paragraph','text':str}
- {'type':'blockquote','text':str}
- {'type':'list','ordered':bool,'items':[...]}
  where each item is {'text': str, 'children': [list_node...]}
"""

from lexer import tokenize


def _build_list(tokens, i):
    """Build one list (possibly nested) starting at tokens[i] (a list_item).

    Items at the starting indent become entries; deeper-indent list_items
    become nested 'list' children inside the most recent item.
    Returns (list_node, new_index).
    """
    base_indent = tokens[i]['indent']
    ordered = tokens[i]['ordered']
    items = []

    while i < len(tokens) and tokens[i]['type'] == 'list_item' and tokens[i]['indent'] >= base_indent:
        tok = tokens[i]
        if tok['indent'] == base_indent:
            items.append({'text': tok['text'], 'children': []})
            i += 1
        else:
            # Deeper -> recurse and attach to last item.
            child, i = _build_list(tokens, i)
            if items:
                items[-1]['children'].append(child)
            else:
                # No parent yet -- treat as new top list (degenerate input).
                items.append({'text': '', 'children': [child]})

    return {'type': 'list', 'ordered': ordered, 'items': items}, i


def parse(text: str):
    tokens = tokenize(text)
    nodes = []
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        t = tok['type']

        if t == 'blank':
            i += 1
            continue

        if t == 'header':
            nodes.append({'type': 'header', 'level': tok['level'], 'text': tok['text']})
            i += 1
            continue

        if t == 'fenced_code':
            nodes.append({'type': 'code', 'lang': tok['lang'], 'text': tok['text']})
            i += 1
            continue

        if t == 'blockquote':
            nodes.append({'type': 'blockquote', 'text': tok['text']})
            i += 1
            continue

        if t == 'list_item':
            list_node, i = _build_list(tokens, i)
            nodes.append(list_node)
            continue

        if t == 'paragraph':
            # Merge consecutive paragraph lines into one paragraph (joined by space).
            buf = [tok['text']]
            i += 1
            while i < len(tokens) and tokens[i]['type'] == 'paragraph':
                buf.append(tokens[i]['text'])
                i += 1
            nodes.append({'type': 'paragraph', 'text': ' '.join(buf)})
            continue

        i += 1

    return nodes
