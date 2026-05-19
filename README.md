# &ocy;&bcy;&lcy;&ocy;&mcy;&kcy;&icy;

Tool to edit font files to replace given word *fragments* by defined
replacements.

## Installation

``` sh
$ sudo apt-get install git python3-fontforge
$ git clone https://github.com/divVerent/oblomki
$ cd oblomki
```

## Usage

Edit `config.py` to contain the replacement rules you want. See
[examples/config.py](examples/config.py) for a nice example.

Then run:

``` sh
$ ./oblomki.py config.py font.ttf font_processed.ttf
```

## Examples

The "GNU FreeFont" fonts processed by this tool are available in
[examples/](https://github.com/divVerent/oblomki/tree/gh-pages/examples).
You can apply them to a browser tab by installing and running the
following bookmarklet:

    javascript:{ let e = document.createElement('link'); e.rel = 'stylesheet'; e.type = 'text/css'; e.href = 'https://divverent.github.io/oblomki/examples/style.css'; document.head.appendChild(e); }

To install a bookmarklet, you copy the above text to the clipboard, add
a new bookmark, and paste it into the bookmark URL. After pasting, check
that it still starts with `javascript:`, and if not, add it back by
hand. Clicking the bookmark then will apply the font to the currently
loaded page - which is especially fun on satire sites like
<http://kremlin.ru> or <https://ria.ru>.

## Why the name?

It literally operates on *fragments*. Also:

<a href="http://www.youtube.com/watch?v=cu7ot1dnvdw"><img src="https://img.youtube.com/vi/cu7ot1dnvdw/0.jpg" width="45%" height="45%" alt="Фріоніс - DEBRIS🔥 (animation)" title="Фріоніс - DEBRIS🔥 (animation)"></a>
<a href="http://www.youtube.com/watch?v=dHzGNrHld_s"><img src="https://img.youtube.com/vi/dHzGNrHld_s/0.jpg" width="45%" height="45%" alt="Freeonis [ENG SUB] - DEBRIS🔥 (animation)" title="Freeonis [ENG SUB] - DEBRIS🔥 (animation)"></a>

## Automated Tests

To run automated tests, run:

``` sh
$ sudo apt-get install dwdiff grep libharfbuzz-bin tar w3m
$ git submodule update --init
$ make -C test
```

## License

This software, like FontForge, is under the [GPL-3](COPYING).
