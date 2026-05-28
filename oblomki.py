#!/usr/bin/env python3
# обломки - Tool to edit font files to replace given word *fragments*.
# Copyright (C) 2026  Rudolf "divVerent" Polzer
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import fontforge
import os
import sys
import tempfile
import itertools
import runpy
import shutil


def chars_to_glyphset(font, chars):
    out = list(
        filter(
            None,
            (
                (font[ord(char)].glyphname if ord(char) in font else None)
                for char in chars
            ),
        )
    )
    if not out:
        return None
    return out


def string_to_glyphsetlist(font, string):
    if callable(string):
        out = string(font)
        if out is None:
            return None
        return [[glyph for glyph in glyphset] if glyphset else None for glyphset in out]
    else:
        return [chars_to_glyphset(font, char) for char in string]


def string_to_glyphset(font, string):
    out = string_to_glyphsetlist(font, string)
    if out is None or None in out:
        return None
    return list(map(set, out))


def string_to_glyphs(font, string):
    out = string_to_glyphsetlist(font, string)
    if out is None or None in out:
        return None
    return list(map(lambda glyphs: glyphs[0], out))


def can_add_class(existing, to_add):
    for i, s in enumerate(existing):
        if s == to_add:
            return True, i
        if s & to_add:
            return False, i
    return True, None


def common_element(target, index):
    prefix = None
    for glyphsets in target:
        try:
            glyphset = glyphsets[index]
        except IndexError:
            return None
        if not glyphset:
            raise Exception("empty glyphset should have been rejected earlier")
        if prefix is None:
            prefix = glyphset
            continue
        if glyphset != prefix:
            return None
    return prefix


def simplify_replacement(backwards, match, forward, target):
    # Do not simplify further than 1 character. No need for an empty glyph.
    # Also, if the match is empty, replacements cannot work either.
    while len(target) > 1 and len(match) > 1:
        prefix = common_element([match, [set([glyph]) for glyph in target]], 0)
        if prefix is None:
            break
        if not can_add_class(backwards, prefix):
            break
        backwards.append(prefix)
        match = match[1:]
        target = target[1:]
    while len(target) > 1 and len(match) > 1:
        suffix = common_element([match, [set([glyph]) for glyph in target]], -1)
        if suffix is None:
            break
        can_add, _ = can_add_class(forward, suffix)
        if not can_add:
            break
        forward.insert(0, suffix)
        match = match[:-1]
        target = target[:-1]
    return backwards, match, forward, target


def replacement_to_glyphs(font, replacement):
    backwards, match, forward, targets = replacement
    backwards = string_to_glyphset(font, backwards)
    match = string_to_glyphset(font, match)
    forward = string_to_glyphset(font, forward)
    targets = filter(
        lambda glyphs: glyphs is not None,
        (string_to_glyphs(font, target) for target in targets),
    )
    target = next(targets, None)
    if backwards is None or match is None or forward is None or not target:
        return None
    backwards, match, forward, target = simplify_replacement(
        backwards, match, forward, target
    )
    return backwards, match, forward, target


def replacements_to_glyphs(font, replacements):
    return list(
        filter(
            None,
            (replacement_to_glyphs(font, replacement) for replacement in replacements),
        )
    )


NAME_PREFIX = "oblomki"


long_to_short_name = {}
short_to_long_name = {}
CHARSET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz._"


def increment(name):
    pos = CHARSET.find(name[-1])
    if pos < 0:
        return name[:-1] + CHARSET[0]
    elif pos == len(CHARSET) - 1:
        return increment(name[:-1]) + CHARSET[0]
    else:
        return name[:-1] + CHARSET[pos + 1]


def shorten_name(name):
    if len(name) < 31:
        return name
    if name in long_to_short_name:
        return long_to_short_name[name]
    short_name = name[:31]
    while short_name in short_to_long_name:
        short_name = increment(short_name)
    short_to_long_name[short_name] = name
    long_to_short_name[name] = short_name
    return short_name


def encode_name(obj):
    # This is a subset of bencode, chosen at random for this purpose.
    # Using _ for strings though as : is not allowed in glyph names.
    if isinstance(obj, list) or isinstance(obj, tuple):
        return f'l{"".join(map(encode_name, obj))}e'
    elif isinstance(obj, set):
        return f'l{"".join(map(encode_name, sorted(obj)))}e'
    elif isinstance(obj, str):
        return f"{len(obj)}_{obj}"
    else:
        raise Exception(f"Unsupported object type: {obj}")


def make_name(title, *components):
    return NAME_PREFIX + "_" + title + "_" + shorten_name(encode_name(components))


def to_classes(groups):
    # First check classes do not overlap.
    classes = [set()]  # Initially empty class for Fontforge.
    indexes = []
    for group in groups:
        if not group:
            raise Exception("empty class detected")
        group_cls = set(group)
        can_add, index = can_add_class(classes, group_cls)
        if not can_add:
            raise Exception(
                f"partially overlapping classes detected: {classes[index]} and {group_cls}"
            )
        if index is None:
            index = len(classes)
            indexes.append(index)
            classes.append(group_cls)
        else:
            indexes.append(index)
    return list(map(sorted, classes)), list(map(str, indexes))


class LigatureSet(object):
    def __init__(self):
        self.existing_full = set()
        self.existing_prefixes = set()

    def to_key(s):
        return make_name("", s)

    def can_add(self, new):
        # Is new a prefix of something already added?
        if LigatureSet.to_key(new) in self.existing_prefixes:
            return False

        # Has a prefix of new already been added?
        for i in range(0, len(new) + 1):
            if LigatureSet.to_key(new[:i]) in self.existing_full:
                return False

        # Otherwise go ahead.
        return True

    def add(self, new):
        for i in range(1, len(new) + 1):
            self.existing_prefixes.add(LigatureSet.to_key(new[:i]))
        self.existing_full.add(LigatureSet.to_key(new))


def process_font(config, infile, outfile):
    font = fontforge.open(infile)

    preprocessed = None
    if "preprocess" in config:
        preprocessed = config["preprocess"](font)

    replacements = replacements_to_glyphs(font, config["replacements"])
    all_glyphs = set(
        (
            glyph
            for backwards, match, forward, unused_target in replacements
            for glyph in set().union(*backwards, *match, *forward)
        )
    )
    print(f"Glyphs matched: {sorted(all_glyphs)}")
    scripts = [
        (script, ["dflt"])
        for script in sorted(
            set(["DFLT"]).union(set((font[glyph].script for glyph in all_glyphs)))
        )
    ]
    print(f"Scripts matched: {scripts}")

    liga_to_table = {}
    liga_tables = {}
    calt = make_name("calt")
    if replacements:
        font.addLookup(calt, "gsub_contextchain", (), [("calt", scripts)])
    for backwards, match, forward, target in replacements:
        liga = make_name("liga", match, target)
        combined = make_name("glyph", target)
        if liga in liga_to_table:
            liga_table = liga_to_table[liga]
        else:
            # We can optimize here.
            # Two matches can be in the same ligature subtable if:
            # - Either: match and target are common (here already done).
            # - Or: the other subtable contains no match that's a substring _or_
            #   a superstring of this one.
            # Thus, best done by collecting previously added ligature tables,
            # and updating the "liga" field if matching.
            for name, ligatures in liga_tables.items():
                if ligatures.can_add(match):
                    liga_table = name
                    liga_subtable = (
                        liga_table + "_sub"
                    )  # Exceeds length, but who cares.
                    break
            else:
                liga_table = liga
                liga_tables[liga_table] = LigatureSet()
                font.addLookup(liga, "gsub_ligature", (), [])
                liga_subtable = liga_table + "_sub"  # Exceeds length, but who cares.
                font.addLookupSubtable(liga, liga_subtable)
            liga_to_table[liga] = liga_table
            liga_tables[liga_table].add(match)

            if len(target) == 1:
                glyph = font[target[0]]
            elif combined in font:
                glyph = font[combined]
            else:
                glyph = font.createChar(-1, combined)
                xoffset = 0
                for srcglyph in target:
                    glyph.addReference(srcglyph, [1, 0, 0, 1, xoffset, 0])
                    xoffset += font[srcglyph].width
                glyph.width = xoffset
                glyph.removeOverlap()
                glyph.autoHint()
                glyph.autoInstr()
            for single_match in itertools.product(*match):
                glyph.addPosSub(liga_subtable, single_match)
        bclasses, bindexes = to_classes(backwards)
        mclasses, mindexes = to_classes(match)
        fclasses, findexes = to_classes(forward)
        brule = " ".join(bindexes)
        mrule = " ".join([mindexes[0], f"@<{liga_table}>"] + mindexes[1:])
        frule = " ".join(findexes)
        rule = " | ".join([brule, mrule, frule])
        calt_subtable = make_name("calt", backwards, match, forward)
        font.addContextualSubtable(
            calt,
            calt_subtable,
            "class",
            rule,
            bclasses=bclasses,
            mclasses=mclasses,
            fclasses=fclasses,
        )
    print(
        f"Added {len(liga_tables)} ligature tables for {len(replacements)} replacements."
    )

    postprocessed = None
    if "postprocess" in config:
        postprocessed = config["postprocess"](font)

    if preprocessed or replacements or postprocessed:
        font.generate(outfile)
        print(f"Successfully processed: {font.fontname}")
    else:
        if infile != outfile:
            # Copy the file as-is, instead of having FontForge write it.
            # That way, if anything incompatible is in it, it won't be affected.
            shutil.copyfile(infile, outfile)
        print(f"No changes applied to {font.fontname}")

    font.close()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(
            f"Usage: {sys.argv[0]} config.py infile.ttf [outfile.ttf]", file=sys.stderr
        )
        sys.exit(1)

    configpath = sys.argv[1]
    infile = sys.argv[2]
    outfile = sys.argv[3] if len(sys.argv) > 3 else infile

    try:
        path = sys.path
        sys.path.insert(0, os.path.dirname(configpath))
        config = runpy.run_path(configpath)
    finally:
        sys.path = path

    process_font(config, infile, outfile)
