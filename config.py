"""Config file for oblomki.

Defines how fonts are to be processed.

See examples/config.py for a more elaborate example.
"""


def preprocess(font):
    """What to do with the font before processing, right after loading.

    Arguments:
    font -- The fontforge.Font object representing the font.
    """
    pass


"""List of replacement rules of the form:

(lookbehind, match, lookahead, replacement)

Where:

lookbehind -- A "matchstring", as defined below. These must occur before a match, but are not replaced.
match -- A "matchstring", as defined below. These are matched and replaced.
lookahead -- A "matchstring", as defined below. These must occur after a match, but are not replaced.
replacement -- An iterable of "matchstring"s, as defined below.

And:

A "matchstring" is one of:
- A callable that takes a fontforge.Font object and return an iterable (string)
  of iterables (character classes) of glyph names in that font.
- A Unicode string.
- An iterable (string) of iterables of Unicode characters (character classes).
- None.

It is "supported" by a font if one of, respectively:
- It is a callable and returns non-None.
- All its characters exist in the font.
- All its elements are character classes of which at least one character exists
  in the font.

Each rule is processed as follows:

- If lookbehind, match, lookahead are not supported by the font, skip.
- From replacement, the first entry supported by the font is chosen.
  - If none exists, skip.
- For every character class in replacement:
  - The first item that exists in the font is chosen.
- Edit the font such that any sequence of lookbehind, match, lookahead becomes:
  - The string that matched lookbehind,
  - the chosen replacement,
  - the string that matched lookahead.
"""
replacements = []


def postprocess(font):
    """What to do with the font after processing, right before saving.

    Arguments:
    font -- The fontforge.Font object representing the font.
    """
    pass
