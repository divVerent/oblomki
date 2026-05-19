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

"""List of replacement rules."""
replacements = [
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
] + [
    ([], "Рос", "", [with_flies("рос"), "рос"]),
    ([separators], "РОС", "", [with_flies("рос"), "рос"]),
    ([], "Rus", "s", [with_flies("rus"), "rus"]),
    ([separators], "RUS", "S", [with_flies("rus"), "rus"]),
    # While at it, also fix some common typos.
    ([], "Киев", [separators], ["Київ"]),
    ([separators], "киев", [separators], ["Київ"]),
    ([], "Киева", [separators], ["Києва"]),
    ([separators], "киева", [separators], ["Києва"]),
    ([], "Киеву", [separators], ["Києву"]),
    ([separators], "киеву", [separators], ["Києву"]),
    ([], "Киевом", [separators], ["Києвом"]),
    ([separators], "киевом", [separators], ["Києвом"]),
    ([], "Киеве", [separators], ["Києву"]),
    ([separators], "киеве", [separators], ["Києву"]),
    ([], "Kiev", [], ["Kyiv"]),
    ([separators], "kiev", [], ["Kyiv"]),
    ([], "Kiew", [], ["Kyjiw"]),
    ([separators], "kiew", [], ["Kyjiw"]),
]


def postprocess(font):
    """What to do with the font after processing, right before saving."""
    pass
