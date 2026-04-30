#!/usr/bin/env python3
# обломки finder - Tool to identify language detecting word fragments.
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

from collections import defaultdict
import logging
import re
import sys
import unicodedata

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)


WORDS = re.compile(r"\w+")


def remove_marks(text):
    return "".join(
        c for c in unicodedata.normalize("NFD", text) if unicodedata.category(c) != "Mn"
    )


def get_words(filename):
    words = set()
    with open(filename, "r") as f:
        for line in f:
            line = remove_marks(line)
            for word in WORDS.findall(line):
                words.add(word)
    return words


def get_oblomki(words, maxlen):
    oblomki = defaultdict(int)
    for word in words:
        for sublen in range(1, maxlen + 1):
            if sublen > 1:
                # at start?
                oblomki[" " + word[0 : sublen - 1]] += 1
                # at end?
                oblomki[word[-(sublen - 1) :] + " "] += 1
            # in the middle?
            for start in range(0, len(word) - sublen + 1):
                oblomki[word[start : start + sublen]] += 1
    return dict(oblomki)


def pick_oblomki(oblomki, counts, fragcount):
    def sortkey(oblomok):
        return (len(oblomok), -counts[oblomok], oblomok)

    result = set()
    for oblomok in sorted(oblomki, key=sortkey):
        if any(
            (
                oblomok[start:end] in result
                for start in range(0, len(oblomok))
                for end in range(start + 1, len(oblomok) + 1)
            )
        ):
            continue
        result.add(oblomok)

    def topkey(oblomok):
        return (-counts[oblomok], len(oblomok), oblomok)

    return sorted(sorted(result, key=topkey)[:fragcount], key=sortkey)


maxlen, fragcount, *files = sys.argv[1:]
maxlen = int(maxlen)
fragcount = int(fragcount)

include = True
include_oblomki = defaultdict(int)
exclude_oblomki = set()
for file in files:
    if file == "--":
        include = not include
        continue
    logging.info("Reading and word splitting %s...", file)
    words = get_words(file)
    logging.info("Identifying oblomki in %s...", file)
    oblomki = get_oblomki(words, maxlen)
    if include:
        logging.info("Merging %s into includes...", file)
        for oblomok, count in oblomki.items():
            include_oblomki[oblomok] += count
    else:
        logging.info("Merging %s into excludes...", file)
        exclude_oblomki.update(oblomki.keys())
logging.info("Computing set difference...")
oblomki = set(include_oblomki.keys()) - exclude_oblomki
logging.info("Picking oblomki...")
oblomki = pick_oblomki(oblomki, include_oblomki, fragcount)

logging.info("Generating output...")
print("OBLOMKI = [")
for oblomok in oblomki:
    print(f'    "{oblomok}",  # {include_oblomki[oblomok]}')
print("]")
