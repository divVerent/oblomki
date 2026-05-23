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
    leftpad = sorted(leftpads)[int(len(leftpads) / 2)]
    rightpad = sorted(rightpads)[int(len(leftpads) / 2)]

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
    width_adjust = 0.5 * width * (1.0 - width_factor)

    # Set left and right side bearing.
    glyph.left_side_bearing = round(leftpad * bearing_factor - width_adjust)
    glyph.width = round((leftpad + rightpad) * bearing_factor + width * width_factor)

    # Create hints.
    glyph.removeOverlap()
    glyph.autoHint()
    glyph.autoInstr()


def preprocess(font):
    """What to do with the font before processing, right after loading."""
    import_svg(font, "oblomki_tryzub", "data/tryzub.svg", 1.0, 0.0, 1.0, 1.0)
    import_svg(font, "oblomki_fly1", "data/fly1.svg", 0.38, 0.61, 0.0, 0.0)
    import_svg(font, "oblomki_fly2", "data/fly2.svg", 0.41, 0.55, 0.0, 0.0)


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
        if ipref != opref:
            result.append(([separators], ipref, suffix, [opref]))
    else:
        result.append(([separators], ipref_lower, suffix, [opref]))
        if ipref != opref:
            result.append(([], ipref, suffix, [opref]))
    return result


def declined(inom, onom, istem=None, ostem=None, stem_suffix=[set("ауоеыи")]):
    if istem is None:
        istem = inom
    if ostem is None:
        ostem = onom
    result = []
    if inom == istem and onom == ostem and len(stem_suffix) == 0:
        # Nominative same as stem? Let's just use one rule.
        result.extend(prefix(istem, ostem, []))
    elif inom == istem and onom == ostem and len(stem_suffix) == 1:
        # Nominative same as stem? Let's just use one rule.
        result.extend(prefix(istem, ostem, [stem_suffix[0] | separators]))
    else:
        # Need stem_suffix to not match before the other rule.
        # TODO: divVerent - can we get a fixed order so stem_suffix is not needed?
        result.extend(prefix(inom, onom, [separators]))
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
        prefix("Украин", "Україн"),
        [
            ([separators], "на Украине", [separators], ["в Україне"]),
            ([separators], "на украине", [separators], ["в Україне"]),
            ([separators], "the Ukraine", [separators], ["Ukraine"]),
            ([separators], "the ukraine", [separators], ["Ukraine"]),
        ],
        prefix("Ukrain", "Ukrain"),  # This rule fixes case only.
        #
        # https://en.wikipedia.org/wiki/KyivNotKiev
        #
        # Let's sort by English correct name, as we gotta sort by _something_.
        #
        declined("Донецк", "Донецьк"),
        #
        declined("Франковск", "Франківськ"),  # No Ivano- due to separator.
        prefix("Frankovsk", "Frankivsk"),
        prefix("Frankowsk", "Frankiwsk"),
        #
        declined("Харьков", "Харків", ostem="Харков"),
        prefix("Kharkov", "Kharkiv"),
        prefix("Charkov", "Charkiv"),
        #
        declined("Киев", "Київ", ostem="Києв"),
        prefix("Kiev", "Kyiv"),
        prefix("Kiew", "Kyjiw"),
        #
        declined("Львов", "Львів", ostem="Львов"),
        prefix("Lvov", "Lviv"),
        prefix("Lwow", "Lwiw"),
        #
        declined("Николаев", "Миколаїв", ostem="Миколаєв"),
        prefix("Nikolaev", "Mykolaiv"),
        prefix("Nikolayev", "Mykolaiv"),
        prefix("Nikolajew", "Mykolajiw"),
        #
        prefix("Одесс", "Одес"),
        prefix("Odessa", "Odesa"),
        #
        prefix("Ровн", "Рівн"),
        prefix("Rovno", "Rivne"),
        prefix("Rowno", "Riwne"),
    )
)


def postprocess(font):
    """What to do with the font after processing, right before saving."""
    pass
