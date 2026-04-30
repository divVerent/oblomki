#!/bin/bash
# обломки finder - Tool to identify russian detecting word fragments.
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

set -ex

fetch() {
	rm -rf words
	mkdir words

	curl -Lo words/belarusian      https://github.com/eymenefealtun/all-words-in-all-languages/raw/refs/heads/main/Belarusian/Belarusian.txt
	curl -Lo words/russian         https://github.com/kkrypt0nn/wordlists/raw/refs/heads/main/wordlists/languages/russian.txt

	curl -Lo words/bulgarian       https://github.com/miglen/bulgarian-wordlists/raw/refs/heads/master/wordlists/all-cyrillic.txt
	curl -Lo words/kazakh          https://github.com/eymenefealtun/all-words-in-all-languages/raw/refs/heads/main/Kazakh/Kazakh.txt
	curl -Lo words/kyrgyz          https://github.com/eymenefealtun/all-words-in-all-languages/raw/refs/heads/main/Kyrgyz/Kyrgyz.txt
	curl -Lo words/macedonian      https://github.com/whoeverest/macedonian-words/raw/refs/heads/master/MK-dict.txt
	curl -Lo words/mongolian       https://github.com/eymenefealtun/all-words-in-all-languages/raw/refs/heads/main/Mongolian/Mongolian.txt
	curl -Lo words/serbo-croatian  https://github.com/tperich/serbian-wordlists/raw/refs/heads/master/serbian-vocab-latin-cyrillic-938k.txt
	curl -Lo words/tajik           https://github.com/eymenefealtun/all-words-in-all-languages/raw/refs/heads/main/Tajik/Tajik.txt
	curl -Lo words/ukrainian       https://github.com/kkrypt0nn/wordlists/raw/refs/heads/main/wordlists/languages/ukrainian.txt
	curl -Lo words/ukrainian.bible https://github.com/Beblia/Holy-Bible-XML-Format/raw/refs/heads/master/UkrainianTUBBible.xml

	git clone --depth=1 https://github.com/typiconman/ponomar words/.church-slavonic
	cat words/.church-slavonic/Ponomar/languages/cu/bible/elis/*.text > words/church-slavonic
}

if ! [ -d words ]; then
	fetch
fi

WORDLISTS_BAD='
	words/russian
'
WORDLISTS_GOOD='
	words/belarusian
	words/bulgarian
	words/church-slavonic
	words/kazakh
	words/kyrgyz
	words/macedonian
	words/mongolian
	words/serbo-croatian
	words/tajik
	words/ukrainian
	words/ukrainian.bible
'
{
	echo "# This is a generated file. Do not edit. Run $0 to regenerate."
	echo
	./oblomki_finder.py 9 256 $WORDLISTS_BAD -- $WORDLISTS_GOOD
} > oblomki_found.py
