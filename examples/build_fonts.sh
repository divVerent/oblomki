#!/bin/sh
# обломки builder - Tool to rebuild the GNU FreeFont with Oblomki family.
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

git submodule update --init

out=$(mktemp -d -t oblomki.XXXXXX)

d0=$(pwd)
for project in autocorrect oblomki theire; do
	cd "$d0/$project"
	for dir in otf ttf woff; do
		mkdir -p "$out"/"$project"/"$dir"
	done
	cat ../freefont/COPYING > "$out"/"$project"/COPYING
	{
		echo "This directory contains GNU FreeFont, edited using обломки's $project example."
		echo
		cat ../freefont/CREDITS
	} > "$out"/"$project"/CREDITS
	suffix=
	for font in ../freefont/otf/*.otf ../freefont/ttf/*.ttf ../freefont/woff/*.woff; do
		outfont="$out"/"$project"/"${font#../freefont/}"
		srcfamily=$(fc-query -f '%{family[0]}\n' "$font" || true)
		python3 ../../oblomki.py config.py "$font" "$outfont"
		if [ -n "$srcfamily" ]; then
			dstfamily=$(fc-query -f '%{family[0]}\n' "$outfont")
			echo "$srcfamily -> $dstfamily"
			dstsuffix=${dstfamily#$srcfamily}
			[ -n "$dstsuffix" ]
			if [ -n "$suffix" ]; then
				[ x"$suffix" = x"$dstsuffix" ]
			else
				suffix=$dstsuffix
			fi
		fi
	done
	[ -n "$suffix" ]
	../build_css.sh web "$out"/"$project" "$suffix"
done
cd "$d0"

cat <<EOF
Processed fonts are in $out/.
To upload, run:

git checkout gh-pages
rsync -vaSHPAX $out/. .
git commit -a
git push
EOF
