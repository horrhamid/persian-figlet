# Persian Figlet (Python)

Figlet-style ASCII art for Persian (Farsi) text with contextual shaping and RTL handling. Python port of [`moh3n9595/persian-figlet`](https://github.com/moh3n9595/persian-figlet).

## Install

```bash
pip install persian-figlet
```

## Usage

### CLI

```bash
persian-figlet "سلام"
```

Options:
- `--font standard` – font name or path to a JSON font file
- `--silent` – suppress console output

### API

```python
from persian_figlet import render

# Prints to stdout
render("سلام")

# Returns the ASCII art string
art = render("سلام", silent=True)
```

## Development

- Install dev tools: `python -m pip install -e .[dev]` (or just `pip install -e .` if you only need the package).
- Run tests: `python -m pytest`

## License

MIT License. Original work by Mohsen Madani; Python port by Hamidreza Sadeghi.
