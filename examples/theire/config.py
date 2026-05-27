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
    []
    # The gimmick is that every word sequence here is correct per se.
    # But mixing them up is wrong in context.
    + cycle("accept", "except")
    + cycle("advice", "advise")
    + cycle("affect", "effect")
    + cycle("could of", "could've")
    + cycle("farther", "further")
    + cycle("its", "it's")
    + cycle("loose", "lose")
    + cycle("principal", "principle")
    + cycle("then", "than")
    + cycle("there", "their", "they're")
    + cycle("went", "gone")
    + cycle("your", "you're")
)


def postprocess(font):
    """What to do with the font after processing, right before saving."""
    pass
