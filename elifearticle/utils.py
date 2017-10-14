import re
import os
from git import Repo

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

def is_year_numeric(value):
    # True if all digits
    if value and re.match("^[0-9]+$", value):
        return True
    return False

def version_from_xml_filename(filename):
    "extract the numeric version from the xml filename"
    try:
        filename_parts = filename.split(os.sep)[-1].split('-')
    except AttributeError:
        return None
    if len(filename_parts) == 3:
        try:
            return int(filename_parts[-1].lstrip('v').rstrip('.xml'))
        except ValueError:
            return None
    else:
        return None

def get_last_commit_to_master():
    """
    returns the last commit on the master branch. It would be more ideal to get the commit
    from the branch we are currently on, but as this is a check mostly to help
    with production issues, returning the commit from master will be sufficient.
    """
    repo = Repo(".")
    last_commit = None
    try:
        last_commit = repo.commits()[0]
    except AttributeError:
        # Optimised for version 0.3.2.RC1
        last_commit = repo.head.commit
    return str(last_commit)

def calculate_journal_volume(pub_date, year):
    """
    volume value is based on the pub date year
    pub_date is a python time object
    """
    try:
        volume = str(pub_date.tm_year - year + 1)
    except:
        volume = None
    return volume

def author_name_from_json(author_json):
    "concatenate an author name from json data"
    author_name = None
    if author_json.get('type'):
        if author_json.get('type') == 'group' and author_json.get('name'):
            author_name = author_json.get('name')
        elif author_json.get('type') == 'person' and author_json.get('name'):
            if author_json.get('name').get('preferred'):
                author_name = author_json.get('name').get('preferred')
    return author_name

def text_from_affiliation_elements(department, institution, city, country):
    "format an author affiliation from details"
    text = ""
    for element in (department, institution, city, country):
        if text != "":
            text += ", "
        if element:
            text += element
    return text
