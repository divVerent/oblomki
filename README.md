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
`[examples/config.py](examples/config.py)` for a nice example.

Then run:

``` sh
$ ./oblomki.py config.py font.ttf font_processed.ttf
```

## Examples

The "GNU FreeFont" fonts processed by this tool are available in
[examples/](examples/). You can apply them to a browser tab by
installing and running the following bookmarklet:

    javascript:{ let e = document.createElement('link'); e.rel = "stylesheet"; e.type = "text/css"; e.href = "https://divVerent.github.io/oblomki/examples/style.css"; document.head.appendChild(e); e = document.createElement('style'); document.head.appendChild(e); e.sheet.insertRule('* { font-family: "FreeSans with Oblomki" ! important; } pre, textarea { font-family: "FreeMono with Oblomki" ! important; }'); }

## License

This software, like FontForge, is under the [GPL-3](COPYING.md).
