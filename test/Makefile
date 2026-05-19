#!/usr/bin/make
# обломки - Tests to verify russian is modified and Ukrainian is not.
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

CORPORA = f.borussia f.john t.john t.kremlinru t.riaru t.terror

CORPORA_TXT = $(patsubst %,corpus.%.txt,$(CORPORA))
CORPORA_PRE = $(patsubst %,corpus.%.pre,$(CORPORA))
CORPORA_POST = $(patsubst %,corpus.%.post,$(CORPORA))
CORPORA_DWDIFF = $(patsubst %,corpus.%.dwdiff,$(CORPORA))
CORPORA_TEST = $(patsubst %,corpus.%.test,$(CORPORA))

# Never auto delete files.
.SECONDARY:

all: test

pre.ttf:
	ln -snf ../examples/freefont/ttf/FreeSans.ttf pre.ttf

post.ttf: pre.ttf
	cd ../examples && ../oblomki.py config.py ../test/$< ../test/$@

corpus.f.borussia.txt:
	echo ' BORUSSIA DORTMUND ' > $@

corpus.f.john.txt:
	set -e; for i in $$(seq 1 21); do w3m -dump https://biblera.com/uk/ukrainian/john/$$i; done > $@

corpus.t.kremlinru.txt:
	w3m -dump http://kremlin.ru/ > $@

corpus.t.john.txt:
	set -e; for i in $$(seq 1 21); do w3m -dump https://biblera.com/ru/russian-synodal/john/$$i; done > $@

corpus.t.riaru.txt:
	w3m -dump https://ria.ru/ > $@

corpus.t.terror.txt:
	echo ' RUSSIA IS A TERRORIST STATE ' > $@

corpus.%.pre: corpus.%.txt pre.ttf
	hb-shape --show-text --no-positions --no-advances --no-clusters pre.ttf < $< > $@

corpus.%.post: corpus.%.txt post.ttf
	hb-shape --show-text --no-positions --no-advances --no-clusters post.ttf < $< > $@

corpus.%.dwdiff: corpus.%.pre corpus.%.post
	dwdiff -P --start-delete="[-:oblomki:del:" --stop-delete=":-]" --start-insert="{+:oblomki:ins:" --stop-insert=":+}" corpus.$*.pre corpus.$*.post > $@ || true

corpus.t.%.test: corpus.t.%.dwdiff
	grep -o ':oblomki:[^:]*:[^:]*:' $< | sort | uniq -c | grep .  # Expecting matches.
	@echo OK

corpus.f.%.test: corpus.f.%.dwdiff
	grep -o ':oblomki:[^:]*:[^:]*:' $< | sort | uniq -c | { ! grep .; }  # Expecting no matches.
	@echo OK

download: pre.ttf $(CORPORA_TXT)

build: post.ttf

test: $(CORPORA_TEST)

clean:
	$(RM) post.ttf $(CORPORA_PRE) $(CORPORA_POST) $(CORPORA_DWDIFF) $(CORPORA_TEST)

fullclean: clean
	$(RM) pre.ttf $(CORPORA_TXT)
