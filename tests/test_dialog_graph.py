import pytest

from dialog_graph import Dialog, DialogNode, DialogChoice, AnimationRef


def test_reject_missing_child():
    with pytest.raises(ValueError) as excinfo:
        Dialog("ROOT",
               [DialogNode("ROOT", "::text::", AnimationRef.of_image_ids(["::image::"]),
                                [DialogChoice("::text::", "MISSING_CHILD")])])
    assert "Dialog choice leading to missing node: MISSING_CHILD" in str(excinfo.value)


def test_reject_duplicate_ids():
    with pytest.raises(ValueError) as excinfo:
        Dialog("DUPLICATE", [DialogNode("DUPLICATE", "::text::", AnimationRef.of_image_ids(["::image::"]), []),
                             DialogNode("DUPLICATE", "::text::", AnimationRef.of_image_ids(["::image::"]), [])])
    assert "Duplicate node ID found: DUPLICATE" in str(excinfo.value)


def test_reject_missing_root():
    with pytest.raises(ValueError) as excinfo:
        Dialog("MISSING", [DialogNode("::id::", "::text::", AnimationRef.of_image_ids(["::image::"]), [])])
    assert "No node found with ID: MISSING" in str(excinfo.value)


def test_initial_state():
    node = DialogNode("START", "Hello!", AnimationRef.of_image_ids(["::image::"]), [DialogChoice("Good bye!", "START")])
    graph = Dialog("START", [node])
    assert graph.current_node() == node


def test_state_after_making_choice():
    first_node = DialogNode("START", "Hello!", AnimationRef.of_image_ids(["::image::"]),
                            [DialogChoice("Good bye!", "END")])
    second_node = DialogNode("END", "It's over.", AnimationRef.of_image_ids(["::image::"]), [])
    graph = Dialog("START", [first_node, second_node])
    graph.make_choice(0)
    assert graph.current_node() == second_node
