#!/usr/bin/env python3
# обломки - Config file to mess up russian language but not Ukrainian.
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

"""Config file for oblomki.

Defines how fonts are to be processed.

This example matches text of russian language and messes with it a little.
"""

import itertools

from oblomki_found import OBLOMKI


def import_svg(
    font,
    glyphname,
    svg,
    scale_factor=1.0,
    offset_factor=0.0,
    bearing_factor=1.0,
    width_factor=1.0,
):
    if glyphname in font:
        return

    # Figure out the left and right side bearings from median of all characters.
    leftpads = [font[glyph].left_side_bearing for glyph in font]
    rightpads = [font[glyph].right_side_bearing for glyph in font]
    leftpad = int(0.5 + sorted(leftpads)[int(len(leftpads) / 2)] * bearing_factor)
    rightpad = int(0.5 + sorted(rightpads)[int(len(leftpads) / 2)] * bearing_factor)

    # Create the glyph.
    glyph = font.createChar(-1, glyphname)

    # Import the glyph.
    glyph.importOutlines(svg, scale=False)

    # Scale it into the usual bounding box.
    xmin, ymin, xmax, ymax = glyph.boundingBox()
    height = font.ascent + font.descent
    scale = height / (ymax - ymin)
    xadd = -(scale * xmin)
    yadd = -(scale * ymin) - font.descent
    glyph.transform([scale, 0, 0, scale, xadd, yadd])
    width = (xmax - xmin) * scale

    # Transform it further.
    glyph.transform([scale_factor, 0, 0, scale_factor, 0, offset_factor * height])
    width *= scale_factor
    width_adjust = int(0.5 + 0.5 * width * (1.0 - width_factor))

    # Set left and right side bearing.
    glyph.left_side_bearing = leftpad - width_adjust
    glyph.right_side_bearing = rightpad - width_adjust

    # Create hints.
    glyph.removeOverlap()
    glyph.autoHint()
    glyph.autoInstr()


def preprocess(font):
    """What to do with the font before processing, right after loading."""
    import_svg(font, "oblomki_tryzub", "data/tryzub.svg", 1.0, 0.0, 1.0, 1.0)
    import_svg(font, "oblomki_fly1", "data/fly1.svg", 0.38, 0.61, 1.0, 0.0)
    import_svg(font, "oblomki_fly2", "data/fly2.svg", 0.41, 0.55, 1.0, 0.0)


def with_flies(text):
    flies = ["oblomki_fly1", "oblomki_fly2"]

    def flyify(font):
        out = []
        for i, char in enumerate(text):
            if i != 0:
                out.append([flies[i % len(flies)]])
            out.append([font[ord(char)].glyphname])
        return out

    return flyify


separators = set(""" !&*()-=+[{]}|;:'",<.>/?""")


def prefix(ipref, opref, suffix=[]):
    result = []
    ipref_lower = ipref[0].lower() + ipref[1:]
    if ipref == ipref_lower:
        result.append(([separators], ipref, suffix, [opref]))
    else:
        result.append(([separators], ipref_lower, suffix, [opref]))
        result.append(([], ipref, suffix, [opref]))
    return result


def declined(inom, onom, istem=None, ostem=None, stem_suffix=[set("ауоеы")]):
    if istem is None:
        istem = inom
    if ostem is None:
        ostem = onom
    result = []
    if inom != istem or onom != ostem:
        result.extend(prefix(inom, onom, [separators]))
    # Need stem_suffix to not match before the other rule.
    # TODO: divVerent - can we get a fixed order so stem_suffix is not needed?
    result.extend(prefix(istem, ostem, stem_suffix))
    return result


"""List of replacement rules."""
replacements = list(
    itertools.chain(
        [
            (
                [separators] if trigger[0] == " " else [],
                trigger.strip(" "),
                [separators] if trigger[-1] == " " else [],
                [
                    (lambda font: [["oblomki_tryzub"]]),
                    "🔱",
                    "♆",
                    "ψ",
                    "Ψ",
                    "Ѱ",
                    "У",
                    "⫝",
                    "(|)",
                ],
            )
            for trigger in OBLOMKI
        ],
        [
            ([], "Рос", "", [with_flies("рос"), "рос"]),
            ([separators], "РОС", "", [with_flies("рос"), "рос"]),
            ([], "Rus", "s", [with_flies("rus"), "rus"]),
            ([separators], "RUS", "S", [with_flies("rus"), "rus"]),
        ],
        # While at it, also fix some common typos.
        declined("Киев", "Київ", ostem="Києв"),
        prefix("Kiev", "Kyiv"),
        prefix("Kiew", "Kyjiw"),
        declined("Харьков", "Харків", ostem="Харков"),
        prefix("Kharkov", "Kharkiv"),
        prefix("Charkov", "Charkiv"),
    )
)


def postprocess(font):
    """What to do with the font after processing, right before saving."""
    pass
