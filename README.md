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

You can use them to view web pages using the font using the following
means:

- As a Chrome extension:
  <https://chromewebstore.google.com/detail/%D0%BE%D0%B1%D0%BB%D0%BE%D0%BC%D0%BA%D0%B8/haoackkacogjhggljincofbfebmaefon>

  This can be set up to either apply to all websites, or to a set of
  selected ones, or to none by default but you can then click the
  extension icon to enable it on the currently loaded page.

- As a Firefox extension:
  <https://addons.mozilla.org/de/firefox/addon/%D0%BE%D0%B1%D0%BB%D0%BE%D0%BC%D0%BA%D0%B8/>

  This can be set up to either apply to all websites, `.ru` domains
  only, or (on desktop Firefox only) to a set of selected ones.

- As a bookmarklet:

      javascript:{ let e = document.createElement('link'); e.rel = 'stylesheet'; e.type = 'text/css'; e.href = 'https://divverent.github.io/oblomki/examples/oblomki/style.css'; document.head.appendChild(e); }

  To install a bookmarklet, you copy the above text to the clipboard,
  add a new bookmark, and paste it into the bookmark URL. After pasting,
  check that it still starts with `javascript:`, and if not, add it back
  by hand. Clicking the bookmark then will apply the font to the
  currently loaded page - which is especially fun on satire sites like
  the ones shown below.

## Gallery

<a href="https://divverent.github.io/oblomki/screenshots/flibusta.png"><img src="https://divverent.github.io/oblomki/screenshots/flibusta.t.png" alt="flibusta" title="flibusta"></a>
<a href="https://divverent.github.io/oblomki/screenshots/kremlin.png"><img src="https://divverent.github.io/oblomki/screenshots/kremlin.t.png" alt="kremlin" title="kremlin"></a>
<a href="https://divverent.github.io/oblomki/screenshots/ria.png"><img src="https://divverent.github.io/oblomki/screenshots/ria.t.png" alt="ria novosti" title="ria novosti"></a>
<a href="https://divverent.github.io/oblomki/screenshots/rt.png"><img src="https://divverent.github.io/oblomki/screenshots/rt.t.png" alt="russia today" title="russia today"></a>

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
