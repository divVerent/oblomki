#!/bin/sh
# обломки extension packer - Tool to pack the browser extension.
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
# along with this program.  If not, see <https://www.gnu.org/licenss/>.

set -ex

cd extension
git checkout gh-pages
git checkout master
rm -rf data
git archive --format=tar --prefix=data/ ../../.. | tar xvf -
{
	cat data/examples/oblomki/setdefault.css
	sed -e '
		s!: url("\([^"]*\)") format("woff");!: url("chrome-extension://__MSG_@@extension_id__/data/examples/oblomki/\1") format("woff"), url("data/examples/oblomki/\1") format("woff");!
	' < data/examples/oblomki/font.css
} > style.css
zip -9r ../extension.zip \
	manifest.json \
	icon-16.png \
	icon-48.png \
	icon-96.png \
	icon-128.png \
	style.css \
	data/examples/oblomki/woff/*.woff \
	data/examples/oblomki/COPYING \
	data/examples/oblomki/CREDITS
