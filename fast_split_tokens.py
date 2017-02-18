"""Fast ldap.schema.tokenizer.split_tokens

Performance improvement for 10 * 3424 schema lines:

* about 8 times faster on Python 2 (3.24 sec / 0.42 sec)
* about 4 times faster on Python 3 (1.63 sec / 0.38 sec)

Input:
"( 2.5.20.1 NAME 'subschema' AUXILIARY MAY ( dITStructureRules $ nameForms $ dITContentRules $ objectClasses $ attributeTypes $ matchingRules $ matchingRuleUse ) X-ORIGIN ( 'RFC 4512' 'user defined' ) )"

Output:
["(", "2.5.20.1", "NAME", "subschema", "AUXILIARY", "MAY", "(", "dITStructureRules", "nameForms", "dITContentRules", "objectClasses", "attributeTypes", "matchingRules", "matchingRuleUse", ")", "X-ORIGIN", "(", "RFC 4512", "user defined", ")", ")"]

Christian Heimes <christian@python.org>
"""
import re

# either one of:
# * "(" or ")" as single token
# * any string of length >= 1 that does not contain "$", "(", ")",
#   "'" (single quote), or white space
# * any string (including empty string) that starts and ends with "'"
tokens_findall = re.compile(r"[()]|[^'$\s()]+|'.*?'").findall


def fast_split_tokens(s, ignored=None):
    parts = []
    for part in tokens_findall(s):
        # If it starts with a quote, it must end with a quote.
        if part and part[0] == "'":
            part = part[1:-1]
        parts.append(part)
    return parts
