import re

__author__ = 'Régis FLORET'


def micro_template(content, keys):
    """
    Micro template engine. No need use Tornado one
    """
    for k in keys.keys():
        content = re.sub('\{\{[\s+|]' + k + '[\s+|]\}\}', keys[k], content)
    return content

