# Persian Figlet (Python)

Figlet-style ASCII art for Persian (Farsi) text with contextual shaping and RTL handling. This is a Python port of [`moh3n9595/persian-figlet`](https://github.com/moh3n9595/persian-figlet).

## Install

```
pip install .
```

or for development:

```
pip install -e .
```

## Usage

### API

```python
from persian_figlet import render

render("سلام")              # prints to stdout
art = render("سلام", silent=True)  # returns the ASCII art string
```

### CLI

```
persian-figlet "سلام"
```

Options:

- `--font standard` – font name or path to a JSON font file
- `--silent` – suppress console output

## Development notes

- The renderer logic is a direct port of the TypeScript implementation; tests can be added with `pytest`.

## License

MIT License. Original work by Mohsen Madani; Python port by Hamid.
