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

## Why the name?

It literally operates on *fragments*. Also:

- [![&Fcy;&rcy;&iukcy;&ocy;&ncy;&iukcy;&scy; - DEBRIS&#128293;
  (animation)](http://img.youtube.com/vi/cu7ot1dnvdw/0.jpg)](http://www.youtube.com/watch?v=cu7ot1dnvdw "Фріоніс - DEBRIS🔥 (animation)")
- [![Freeonis \[ENG SUB\] - DEBRIS&#128293;
  (animation)](http://img.youtube.com/vi/dHzGNrHld_s/0.jpg)](http://www.youtube.com/watch?v=dHzGNrHld_s "Freeonis [ENG SUB] - DEBRIS🔥 (animation)")

## License

This software, like FontForge, is under the [GPL-3](COPYING.md).
