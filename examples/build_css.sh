#!/bin/sh
# обломки - CSS generator for edited fonts.
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

set -e

if [ $# -ne 3 ]; then
	cat <<EOF >&2
Usage:
  $0 web styledir 'suffix'
  $0 extension stylefile 'suffix'
EOF
	exit 1
fi

mode=$1; shift
out=$1; shift
suffix=$1; shift

to() {
	case "$mode" in
		extension)
			case "$1" in
				font.css)
					sed -e '
						s!: url("\([^"]*\)") format("woff");!: url("chrome-extension://__MSG_@@extension_id__/data/\1") format("woff"), url("data/\1") format("woff");!
					' >"$out"/style.css
					;;
				setdefault.css)
					cat >>"$out"/style.css
					;;
				style.css)
					cat >/dev/null
					;;
			esac
			;;
		web)
			cat >"$out"/"$1"
			;;
	esac
}

to font.css <<EOF
@font-face {
  font-family: "FreeMono$suffix";
  src: url("woff/FreeMono.woff") format("woff");
  font-weight: normal;
  font-style: normal;
}
@font-face {
  font-family: "FreeMono$suffix";
  src: url("woff/FreeMonoBold.woff") format("woff");
  font-weight: bold;
  font-style: normal;
}
@font-face {
  font-family: "FreeMono$suffix";
  src: url("woff/FreeMonoOblique.woff") format("woff");
  font-weight: normal;
  font-style: italic;
}
@font-face {
  font-family: "FreeMono$suffix";
  src: url("woff/FreeMonoBoldOblique.woff") format("woff");
  font-weight: bold;
  font-style: italic;
}
@font-face {
  font-family: "FreeSans$suffix";
  src: url("woff/FreeSans.woff") format("woff");
  font-weight: normal;
  font-style: normal;
}
@font-face {
  font-family: "FreeSans$suffix";
  src: url("woff/FreeSansBold.woff") format("woff");
  font-weight: bold;
  font-style: normal;
}
@font-face {
  font-family: "FreeSans$suffix";
  src: url("woff/FreeSansOblique.woff") format("woff");
  font-weight: normal;
  font-style: italic;
}
@font-face {
  font-family: "FreeSans$suffix";
  src: url("woff/FreeSansOblique.woff") format("woff");
  font-weight: bold;
  font-style: italic;
}
@font-face {
  font-family: "FreeSerif$suffix";
  src: url("woff/FreeSerif.woff") format("woff");
  font-weight: normal;
  font-style: normal;
}
@font-face {
  font-family: "FreeSerif$suffix";
  src: url("woff/FreeSerifBold.woff") format("woff");
  font-weight: bold;
  font-style: normal;
}
@font-face {
  font-family: "FreeSerif$suffix";
  src: url("woff/FreeSerifOblique.woff") format("woff");
  font-weight: normal;
  font-style: italic;
}
@font-face {
  font-family: "FreeSerif$suffix";
  src: url("woff/FreeSerifOblique.woff") format("woff");
  font-weight: bold;
  font-style: italic;
}
EOF

to setdefault.css <<EOF
*:not(
  /* Bootstrap */
  .bi, .bi *,
  [class^="bi-"], [class^="bi-"] *, [class*=" bi-"], [class*=" bi-"] *,
  /* Font Awesome */
  [class^="fa-"], [class^="fa-"] *, [class*=" fa-"], [class*=" fa-"] *,
  .fa, .fa *,
  .fab, .fab *,
  .fad, .fad *,
  .fal, .fal *,
  .far, .far *,
  .fas, .fas *,
  /* Foundation */
  [class^="fi-"], [class^="fi-"] *, [class*=" fi-"], [class*=" fi-"] *,
  /* Glyphicon */
  .glyphicon, .glyphicon *,
  [class^="glyphicon-"], [class^="glyphicon-"] *, [class*=" glyphicon-"], [class*=" glyphicon-"] *,
  /* Open Iconic */
  .oi, .oi *,
  [class^="oi-"], [class^="oi-"] *, [class*=" oi-"], [class*=" oi-"] *,
  /* LineIcons */
  .lni, .lni *,
  [class^="lni-"], [class^="lni-"] *, [class*=" lni-"], [class*=" lni-"] *,
  /* Material Design */
  .mat-icon, .mat-icon *,
  .material-icons, .material-icons *,
  [class^="material-icons-"], [class^="material-icons-"] *, [class*=" material-icons-"], [class*=" material-icons-"] *,
  [class^="material-symbols-"], [class^="material-symbols-"] *, [class*=" material-symbols-"], [class*=" material-symbols-"] *,
  .google-material-icons, .google-material-icons *,
  .google-symbols, .google-symbols *,
  [class^="google-material-icons-"], [class^="google-material-icons-"] *, [class*=" google-material-icons-"], [class*=" google-material-icons-"] *,
  [class^="google-material-symbols-"], [class^="google-material-symbols-"] *, [class*=" google-material-symbols-"], [class*=" google-material-symbols-"] *,
  /* Remix Icon */
  .ri, .ri *,
  [class^="ri-"], [class^="ri-"] *, [class*=" ri-"], [class*=" ri-"] *,
  /* Tabler */
  [class^="ti-"], [class^="ti-"] *, [class*=" ti-"], [class*=" ti-"] *,
  .ti, .ti *,
  /* Vanilla */
  [class^="p-icon-"], [class^="p-icon-"] *, [class*=" p-icon-"], [class*=" p-icon-"] *,
  /* otto.de */
  .p_icons, .p_icons *,
  /* Generic */
  .icon, .icon *,
  [class^="icon-"], [class^="icon-"] *, [class*=" icon-"], [class*=" icon-"] *
) {
  /* By default everything inherits. */
  font-family: inherit ! important;
  /* Apply main font at document root. */
  &:is(:root, html, body, #app) {
    font-family: "FreeSans$suffix" ! important;
  }
  /* Use serif for headlines. */
  &:is(h1, h2, h3, h4, h5, h6) {
    font-family: "FreeSerif$suffix" ! important;
  }
  /* Use mono for code and text input. */
  &:is(pre, textarea, code, input[type="text"], input:not([type])) {
    font-family: "FreeMono$suffix" ! important;
  }
}
EOF

to style.css <<EOF
@import "font.css";
@import "setdefault.css";
EOF
