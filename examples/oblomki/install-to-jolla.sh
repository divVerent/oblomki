#!/bin/sh
# обломки - Script to install oblomkized fonts on a Sailfish OS device.
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

# Usage:
#
# 1. Set up your SSH so `jolla` resolves to your Sailfish OS device.
# 2. Run this script.
# 3. To start font replacement, run:
#    `devel-su -c /root/oblomki.start.sh`
# 4. To stop font replacement, run:
#    `devel-su -c /root/oblomki.stop.sh`
#
# WARNING:
#
# This breaks Android subsystem restarting.
#
# Will figure out a better solution later, but for now:
# - Before stopping/restarting App Support, stop it.
# - After boot or having launched App Support, start it again.
#
# TODO: maybe figure out systemd integration?

set -ex

fontdirs='
	/usr/share/fonts
	/opt/appsupport/rootfs/system/fonts
	/home/.appsupport/instance/defaultuser/data/data/org.lds.ldssa/files/styles/fonts
'
overlayroot=/root/oblomki
overlayscript=/root/oblomki.start.sh
unoverlayscript=/root/oblomki.stop.sh
mountdir=$(mktemp -d -t oblomki.XXXXXX)

LF='
'

ssh root@jolla "
	set -ex;
	overlayscript='$overlayscript';
	unoverlayscript='$unoverlayscript';
"'
	cat > "$overlayscript" <<EOF;
#!/bin/sh

set -ex

EOF
	chmod 755 "$overlayscript";
	cat > "$unoverlayscript" <<EOF;
#!/bin/sh

set -ex

EOF
	chmod 755 "$unoverlayscript";
'

commands=
for fontdir in $fontdirs; do
	overlaydir=$overlayroot$fontdir;

	ssh root@jolla "
		set -ex;
		fontdir='$fontdir';
		overlaydir='$overlaydir';
		overlayscript='$overlayscript';
		unoverlayscript='$unoverlayscript';
	"'
		origdir=$(mktemp -d -t oblomki.XXXXXX);

		mount --bind -o ro "${fontdir%/*}" "$origdir";
		srcdir="$origdir/${fontdir##*/}";

		rm -rf "$overlaydir";
		mkdir -p "$overlaydir";
		cp -aRv "$srcdir/." "$overlaydir";

		umount "$origdir";

		echo "mount --bind '\''$overlaydir'\'' '\''$fontdir'\''" >> "$overlayscript";
		echo "umount -l '\''$fontdir'\''" >> "$unoverlayscript";
	'

	sshfs root@jolla:"$overlaydir" "$mountdir"
	find "$mountdir" \( -iname \*.ttf -o -iname \*.otf \) -print0 | {
		cd oblomki/examples
		xargs -0 -n 1 python3 ../oblomki.py config.py
	}
	umount "$mountdir"
done
