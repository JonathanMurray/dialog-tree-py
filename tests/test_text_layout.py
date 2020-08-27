from constants import Vec2
from dialog_tree import ui


def font_size(text: str) -> Vec2:
    return len(text), 1


def test_simple():
    assert list(ui.layout_text_in_area("AB", font_size, 2)) == ["AB"]


def test_word_boundaries():
    assert list(ui.layout_text_in_area("hello world", font_size, 8)) == ["hello ", "world"]


def test_no_whitespace_at_start_of_line():
    assert list(ui.layout_text_in_area("hello world", font_size, 5)) == ["hello", "world"]


def test_long_word_split():
    lines = ui.layout_text_in_area("hello world", font_size, 4)
    assert next(lines) == "hell"
    assert next(lines) == "o "
    assert next(lines) == "worl"
    assert next(lines) == "d"


def test_complex():
    assert list(ui.layout_text_in_area("This is a long text. It is split onto several lines.", font_size, 10)) \
           == ["This is a ", "long text.", "It is ", "split onto", "several ", "lines."]
