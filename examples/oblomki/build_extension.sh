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

git checkout gh-pages
git pull
git checkout master
cd extension
rm -rf data
git -C .. archive --format=tar --prefix=data/ gh-pages | tar xvf -
../../build_css.sh extension . ' with Oblomki'
zip -9r ../extension.zip \
	manifest.json \
	icon-16.png \
	icon-48.png \
	icon-96.png \
	icon-128.png \
	style.css \
	data/woff/*.woff \
	data/COPYING \
	data/CREDITS
