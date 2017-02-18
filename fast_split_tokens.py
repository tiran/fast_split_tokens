"""Fast ldap.schema.tokenizer.split_tokens

Performance improvement for 10 * 3424 schema lines:

* about 8 times faster on Python 2 (3.24 sec / 0.42 sec)
* about 4 times faster on Python 3 (1.63 sec / 0.38 sec)

Input:
"( 2.5.20.1 NAME 'subschema' AUXILIARY MAY ( dITStructureRules $ nameForms $ dITContentRules $ objectClasses $ attributeTypes $ matchingRules $ matchingRuleUse ) X-ORIGIN ( 'RFC 4512' 'user defined' ) )"

Output:
["(", "2.5.20.1", "NAME", "subschema", "AUXILIARY", "MAY", "(", "dITStructureRules", "nameForms", "dITContentRules", "objectClasses", "attributeTypes", "matchingRules", "matchingRuleUse", ")", "X-ORIGIN", "(", "RFC 4512", "user defined", ")", ")"]

The attached patch file is derived from python-ldap module. All of the
modifications to python-ldap module represented in the following patch(es)
were developed by Christian Heimes <christian@python.org>. I have not
assigned rights and/or interest in this work to any party.
"""
import re

tokens_findall = re.compile(
    r"(\()"           # opening parenthesis
    r"|"              # or
    r"(\))"           # closing parenthesis
    r"|"              # or
    r"([^'$()\s]+)"   # string of length >= 1 without '$() or whitespace
    r"|"              # or
    r"('.*?'(?!\w))"  # any string or empty string surrounded by single quotes
                      # except if right quote is succeeded by alphanumeric char
    r"|"              # or
    r"([^\s]+?)",     # residue, all non-whitespace strings
    re.UNICODE
).findall


def fast_split_tokens(s, keywordDict):
    parts = []
    parens = 0
    for opar, cpar, unquoted, quoted, residue in tokens_findall(s):
        if unquoted:
            parts.append(unquoted)
        elif quoted:
            parts.append(quoted[1:-1])
        elif opar:
            parens += 1
            parts.append(opar)
        elif cpar:
            parens -= 1
            parts.append(cpar)
        elif residue == '$':
            if not parens:
                raise ValueError("'$' outside parenthesis", s)
        else:
            raise ValueError(residue, s)

    if parens:
        raise ValueError("Unbalanced parenthesis in '{}'".format(s))

    return parts
