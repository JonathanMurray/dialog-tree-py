import pytest

from dialog_graph import DialogGraph, DialogNode, DialogChoice


def test_reject_missing_child():
    with pytest.raises(ValueError) as excinfo:
        DialogGraph("ROOT",
                    [DialogNode("ROOT", "::text::", ["::image::"], [DialogChoice("::text::", "MISSING_CHILD")])])
    assert "Dialog choice leading to missing node: MISSING_CHILD" in str(excinfo.value)


def test_reject_duplicate_ids():
    with pytest.raises(ValueError) as excinfo:
        DialogGraph("DUPLICATE", [DialogNode("DUPLICATE", "::text::", ["::image::"], []),
                                  DialogNode("DUPLICATE", "::text::", ["::image::"], [])])
    assert "Duplicate node ID found: DUPLICATE" in str(excinfo.value)


def test_reject_missing_root():
    with pytest.raises(ValueError) as excinfo:
        DialogGraph("MISSING", [DialogNode("::id::", "::text::", ["::image::"], [])])
    assert "No node found with ID: MISSING" in str(excinfo.value)


def test_initial_state():
    node = DialogNode("START", "Hello!", ["::image::"], [DialogChoice("Good bye!", "START")])
    graph = DialogGraph("START", [node])
    assert graph.current_node() == node


def test_state_after_making_choice():
    first_node = DialogNode("START", "Hello!", ["::image::"], [DialogChoice("Good bye!", "END")])
    second_node = DialogNode("END", "It's over.", ["::image::"], [])
    graph = DialogGraph("START", [first_node, second_node])
    graph.make_choice(0)
    assert graph.current_node() == second_node
