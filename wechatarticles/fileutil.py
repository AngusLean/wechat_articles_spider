# encoding=utf-8
"""
Url: https://gist.github.com/wassname/1393c4a57cfcbf03641dbc31886123b8
"""
import unicodedata
import string

valid_filename_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
char_limit = 255

def clean_filename(filename, whitelist=valid_filename_chars, replace=' '):
    # replace spaces
    for r in replace:
        filename = filename.replace(r,'_')

    # keep only valid ascii chars
    cleaned_filename = unicodedata.normalize('NFKD', filename).decode()
    #  .encode('ASCII', 'ignore')

    # keep only whitelisted chars
    cleaned_filename = ''.join(c for c in cleaned_filename if c in whitelist)
    if len(cleaned_filename)>char_limit:
        print("Warning, filename truncated because it was over {}. Filenames may no longer be unique".format(char_limit))
    return cleaned_filename[:char_limit]

def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    import unicodedata
    import re
    #  value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = str(re.sub('[^\w\s-]', '', value).strip().lower())

    value = str(re.sub('[-\s]+', '-', value))
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", value)  # 替换为下划线
    return new_title
    #  return value

