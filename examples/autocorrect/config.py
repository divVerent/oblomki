"""Config file for oblomki.

Defines how fonts are to be processed.

See examples/config.py for a more elaborate example.
"""


def preprocess(font):
    """What to do with the font before processing, right after loading."""
    font.familyname += " with Autocorrect"


separators = set(""" !&*()-=+[{]}|;:'",<.>/?""")


def replacements_from(filename):
    ret = []
    with open(filename, "r") as file:
        for line in file.readlines():
            match, replace = line.split("->", 1)

            replace = [x for x in (x.strip() for x in replace.split(",")) if x != ""]
            if len(replace) != 1:
                continue
            replace = replace[0]

            match_upper = match[0].upper() + match[1:]
            replace_upper = replace[0].upper() + replace[1:]

            if match_upper != match:
                ret.append(([], match_upper, [separators], [replace_upper]))
                ret.append(([separators], match, [separators], [replace]))
            else:
                ret.append(([], match, [separators], [replace]))
    # Keep only some rules. Fonts can't handle much more.
    # Otherwise: Internal Error: Attempt to output 65536 into a 16-bit field. It will be truncated and the file may not be useful.
    n = 5000

    def complexity(rule):
        lookbehind, match, lookahead, replace = rule
        return len(lookbehind) + len(match) + len(lookahead) + len(replace[0])

    ret = sorted(ret, key=complexity)[:n]
    return ret


"""List of replacement rules."""
replacements = replacements_from("typos/crates/wikipedia-dict/assets/dictionary.txt")


def postprocess(font):
    """What to do with the font after processing, right before saving."""
    pass
