"""Config file for oblomki.

Defines how fonts are to be processed.

See examples/config.py for a more elaborate example.
"""


def preprocess(font):
    """What to do with the font before processing, right after loading."""
    pass


separators = set(""" !&*()-=+[{]}|;:'",<.>/?""")


def cycle(*l):
    ret = []
    for i in range(len(l)):
        fr, to = l[i - 1], l[i]
        ret.append(([separators], fr, [separators], [to]))
        ret.append(([], fr[0].upper() + fr[1:], [separators], [to[0].upper() + to[1:]]))
    return ret


"""List of replacement rules."""
replacements = (
    cycle("there", "their", "they're")
    + cycle("a lot", "allot")
    + cycle("accept", "except")
    + cycle("affect", "effect")
)


def postprocess(font):
    """What to do with the font after processing, right before saving."""
    pass
