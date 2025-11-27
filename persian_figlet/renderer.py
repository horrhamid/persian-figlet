from __future__ import annotations

from enum import Enum
from typing import Any, Iterable, List, Mapping, Optional, Sequence, Tuple

from .fonts import load_font

CHAR_HEIGHT = 13
HALF_SPACE_KEY = "__HALF_SPACE__"

NON_CONNECTING_CHARS = {
	"ا",
	"د",
	"ذ",
	"ر",
	"ز",
	"ژ",
	"و",
	"آ",
}


class CharForm(str, Enum):
	ISOLATED = "isolated"
	INITIAL = "initial"
	MEDIAL = "medial"
	FINAL = "final"


def is_persian_char(ch: str) -> bool:
	if not ch:
		return False
	code = ord(ch)
	is_arabic_base = 0x0600 <= code <= 0x06FF
	is_persian_digit = 0x06F0 <= code <= 0x06F9
	return is_arabic_base or is_persian_digit


def can_connect_to_next(ch: str) -> bool:
	return is_persian_char(ch) and ch not in NON_CONNECTING_CHARS


def can_connect_to_prev(ch: str) -> bool:
	return is_persian_char(ch)


def process_text(text: str) -> List[Tuple[str, CharForm]]:
	"""
	Process Persian text into characters with their contextual forms.
	"""
	result: List[Tuple[str, CharForm]] = []
	chars = list(text)

	for i, current in enumerate(chars):
		prev_char = chars[i - 1] if i > 0 else None
		next_char = chars[i + 1] if i < len(chars) - 1 else None

		if current == "\u200C":
			result.append((HALF_SPACE_KEY, CharForm.ISOLATED))
			continue

		if not is_persian_char(current):
			result.append((current, CharForm.ISOLATED))
			continue

		connects_prev = (
			prev_char
			and can_connect_to_prev(current)
			and can_connect_to_next(prev_char)
			and is_persian_char(prev_char)
		)

		connects_next = (
			next_char
			and can_connect_to_next(current)
			and can_connect_to_prev(next_char)
			and is_persian_char(next_char)
		)

		if connects_prev and connects_next:
			form = CharForm.MEDIAL
		elif connects_prev and not connects_next:
			form = CharForm.FINAL
		elif not connects_prev and connects_next:
			form = CharForm.INITIAL
		else:
			form = CharForm.ISOLATED

		result.append((current, form))

		if is_persian_char(current) and next_char and not can_connect_to_next(current):
			result.append((HALF_SPACE_KEY, CharForm.ISOLATED))

	return result


def apply_kerning(
	patterns: Iterable[Tuple[Sequence[str], Mapping[str, int]]]
) -> List[str]:
	if not patterns:
		return [""] * CHAR_HEIGHT

	lines = [""] * CHAR_HEIGHT
	current_position = 0

	for pattern, kerning in patterns:
		start_pos = max(0, current_position + int(kerning.get("left", 0)))

		for row in range(CHAR_HEIGHT):
			current_line = lines[row]
			char_line = pattern[row]
			required_length = start_pos + len(char_line)
			if len(current_line) < required_length:
				current_line = current_line.ljust(required_length)

			new_line = current_line[:start_pos]
			for j, ch in enumerate(char_line):
				pos = start_pos + j
				existing = current_line[pos] if pos < len(current_line) else " "
				new_line += ch if ch != " " else existing

			if start_pos + len(char_line) < len(current_line):
				new_line += current_line[start_pos + len(char_line) :]

			lines[row] = new_line

		char_width = max(len(line) for line in pattern)
		current_position = start_pos + char_width + int(kerning.get("right", 0))

	return lines


def _get_char_definition(
	char: str, form: CharForm, font: Mapping[str, Any]
) -> Mapping[str, Any]:
	entry = font.get(char)
	space_entry = font.get(" ", {})

	if entry:
		variant = entry.get(form.value) or entry.get(CharForm.ISOLATED.value)
		if variant:
			return variant

	if char == HALF_SPACE_KEY and HALF_SPACE_KEY in font:
		half_space = font[HALF_SPACE_KEY]
		variant = half_space.get(form.value) or half_space.get(CharForm.ISOLATED.value)
		if variant:
			return variant

	space_variant = space_entry.get(form.value) or space_entry.get(
		CharForm.ISOLATED.value
	)
	if space_variant:
		return space_variant

	# Final fallback: blank character with no kerning
	return {
		"pattern": [" " * 2] * CHAR_HEIGHT,
		"kerning": {"left": 0, "right": 0},
	}


def render(
	text: str,
	*,
	font: Optional[Mapping[str, Any]] = None,
	font_name: str = "standard",
	silent: bool = False,
) -> str:
	"""
	Render Persian text to ASCII art.

	:param text: Input text
	:param font: Optional pre-loaded font mapping
	:param font_name: Name of packaged font to load when *font* is not provided
	:param silent: When True, suppress console output and only return the art
	"""
	font_data = font or load_font(font_name)
	processed = list(reversed(process_text(text)))

	rendered: List[Tuple[Sequence[str], Mapping[str, int]]] = []
	for char, form in processed:
		entry = _get_char_definition(char, form, font_data)
		rendered.append((entry["pattern"], entry["kerning"]))

	lines = apply_kerning(rendered)
	art = "\n".join(lines)
	if not silent:
		print(art)
	return art
