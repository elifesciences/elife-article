import re

def repl(match):
    "Convert hex to int to unicode character"
    chr_code = int(match.group(1), 16)
    return unichr(chr_code)

def entity_to_unicode(string):
    """
    Quick convert unicode HTML entities to unicode characters
    using a regular expression replacement
    """
    # Selected character replacements that have been seen
    replacements = []
    replacements.append((r"&alpha;", u"\u03b1"))
    replacements.append((r"&beta;", u"\u03b2"))
    replacements.append((r"&gamma;", u"\u03b3"))
    replacements.append((r"&delta;", u"\u03b4"))
    replacements.append((r"&epsilon;", u"\u03b5"))
    replacements.append((r"&ordm;", u"\u00ba"))
    replacements.append((r"&iuml;", u"\u00cf"))
    replacements.append((r"&ldquo;", '"'))
    replacements.append((r"&rdquo;", '"'))

    # First, replace numeric entities with unicode
    string = re.sub(r"&#x(....);", repl, string)
    # Second, replace some specific entities specified in the list
    for entity, replacement in replacements:
        string = re.sub(entity, replacement, string)
    return string

def remove_tag(tag_name, string):
    """
    Remove open and close tags - the tags themselves only - using
    a non-greedy angle bracket pattern match
    """
    if not string:
        return string
    p = re.compile('</?' + tag_name + '.*?>')
    string = p.sub('', string)
    return string

def replace_tags(string, from_tag='i', to_tag='italic'):
    """
    Replace tags such as <i> to <italic>
    <sup> and <sub> are allowed and do not need to be replaced
    This does not validate markup
    """
    string = string.replace('<' + from_tag + '>', '<' + to_tag + '>')
    string = string.replace('</' + from_tag + '>', '</' + to_tag + '>')
    return string

def set_attr_if_value(obj, attr_name, value):
    "shorthand method to set object values if the value is not none"
    if value is not None:
        setattr(obj, attr_name, value)
