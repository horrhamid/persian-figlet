import argparse

from .fonts import load_font
from .renderer import render


def main() -> None:
	parser = argparse.ArgumentParser(
		description="Render Persian text as figlet-style ASCII art"
	)
	parser.add_argument("text", help="Text to render (Persian/Farsi)")
	parser.add_argument(
		"--font",
		default="standard",
		help="Font name (packaged) or path to a JSON font file",
	)
	parser.add_argument(
		"--silent",
		action="store_true",
		help="Suppress console output and only return the string",
	)
	args = parser.parse_args()

	font_data = load_font(args.font)
	render(args.text, font=font_data, silent=args.silent)


if __name__ == "__main__":
	main()
