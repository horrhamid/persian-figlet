import json
from importlib import resources
from pathlib import Path
from typing import Any, Mapping, Union


FontLike = Union[str, Path]


def load_font(font: FontLike = "standard") -> Mapping[str, Any]:
	"""
	Load a font definition.

	- If *font* is a name (e.g., "standard"), it is loaded from the packaged fonts.
	- If *font* looks like a path or ends with ``.json``, it is read from disk.
	"""
	if isinstance(font, Path):
		text = font.read_text(encoding="utf-8")
		return json.loads(text)

	if "/" in font or font.endswith(".json"):
		path = Path(font)
		text = path.read_text(encoding="utf-8")
		return json.loads(text)

	resource = resources.files("persian_figlet").joinpath("fonts", f"{font}.json")
	text = resource.read_text(encoding="utf-8")
	return json.loads(text)
