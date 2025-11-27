from persian_figlet import render


def test_render_smoke() -> None:
	art = render("سلام", silent=True)
	assert isinstance(art, str)
	assert len(art.splitlines()) == 13
	assert "██" in art
