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
zip -9r ../extension.zip \
	manifest.json \
	data/examples/COPYING \
	data/examples/CREDITS \
	data/examples/font.css \
	data/examples/style.css \
	data/examples/woff/*.woff
