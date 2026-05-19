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
    return backwards, match, forward, target


def replacements_to_glyphs(font, replacements):
    return list(
        filter(
            None,
            (replacement_to_glyphs(font, replacement) for replacement in replacements),
        )
    )


NAME_PREFIX = "oblomki"


def make_name(*components):
    return repr([NAME_PREFIX] + list(components))


def to_classes(groups):
    # First check classes do not overlap.
    classes = [set()]  # Initially empty class for Fontforge.
    indexes = []
    for group in groups:
        if not group:
            raise Exception("empty class detected")
        group_cls = set(group)
        for i, cls in enumerate(classes):
            if cls == group_cls:
                indexes.append(i)
                break
            if cls & group_cls:
                raise Exception(
                    "partially overlapping classes detected: {cls} and {group_cls}"
                )
        else:
            i = len(classes)
            indexes.append(i)
            classes.append(group_cls)
    return list(map(sorted, classes)), list(map(str, indexes))


def process_font(config, infile, outfile):
    font = fontforge.open(infile)

    if "preprocess" in config:
        config["preprocess"](font)

    replacements = replacements_to_glyphs(font, config["replacements"])
    all_glyphs = set(
        (
            glyph
            for backwards, match, forward, unused_target in replacements
            for glyph in set().union(*backwards, *match, *forward)
        )
    )
    print(f"Glyphs matched: {all_glyphs}")
    scripts = [
        (script, ["dflt"])
        for script in sorted(
            set(["DFLT"]).union(set((font[glyph].script for glyph in all_glyphs)))
        )
    ]
    print(f"Scripts matched: {scripts}")

    liga_seen = set()
    combined_count = 0
    calt = make_name("calt")
    if replacements:
        font.addLookup(calt, "gsub_contextchain", (), [("calt", scripts)])
    for backwards, match, forward, target in replacements:
        liga = make_name("liga", match, target)
        if liga not in liga_seen:
            liga_seen.add(liga)
            font.addLookup(liga, "gsub_ligature", (), [])
            liga_subtable = make_name("liga", match, target, "sub")
            font.addLookupSubtable(liga, liga_subtable)
            if len(target) == 1:
                glyph = font[target[0]]
            else:
                combined = make_name(combined_count)
                combined_count += 1
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
        mrule = " ".join([mindexes[0], f"@<{liga}>"] + mindexes[1:])
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

    if "postprocess" in config:
        config["postprocess"](font)

    font.generate(outfile)
    print(f"Successfully processed: {font.fontname}")

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
