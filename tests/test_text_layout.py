from dialog_tree import ui


def test_simple():
    assert list(ui.layout_text_in_area("AB", len, 2)) == ["AB"]


def test_word_boundaries():
    assert list(ui.layout_text_in_area("hello world", len, 8)) == ["hello ", "world"]


def test_no_whitespace_at_start_of_line():
    assert list(ui.layout_text_in_area("hello world", len, 5)) == ["hello", "world"]


def test_long_word_split():
    lines = ui.layout_text_in_area("hello world", len, 4)
    assert next(lines) == "hell"
    assert next(lines) == "o "
    assert next(lines) == "worl"
    assert next(lines) == "d"


def test_complex():
    assert list(ui.layout_text_in_area("This is a long text. It is split onto several lines.", len, 10)) \
           == ["This is a ", "long text.", "It is ", "split onto", "several ", "lines."]
