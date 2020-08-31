import pytest

from config_file import parse_dialog_from_json


def test_empty_invalid():
    with pytest.raises(ValueError) as excinfo:
        parse_dialog_from_json({})
    assert "Invalid configuration file!" in str(excinfo.value)


def test_load_simple_sequence():
    dialog_json = {
        "sequence": [
            ["text 1",
             "image 1"],
            ["text 2",
             "image 2"]
        ]
    }
    dialog_graph = parse_dialog_from_json(dialog_json)

    assert dialog_graph.current_node().text == "text 1"
    assert dialog_graph.current_node().graphics.image_ids == ["image 1"]
    assert dialog_graph.current_node().choices[0].text == "Next"
    dialog_graph.make_choice(0)
    assert dialog_graph.current_node().text == "text 2"
    assert dialog_graph.current_node().graphics.image_ids == ["image 2"]
    assert dialog_graph.current_node().choices[0].text == "Play from beginning"


def test_load_graph():
    dialog_json = {
        "graph": {
            "root": "1",
            "nodes": [
                {
                    "id": "1",
                    "text": "text 1",
                    "graphics": {
                        "image": "image 1"
                    },
                    "choices": [
                        [
                            "stay here",
                            "1"
                        ],
                        [
                            "go next",
                            "2"
                        ]
                    ]
                },
                {
                    "id": "2",
                    "text": "text 2",
                    "graphics": {
                        "image": "image 2"
                    },
                    "choices": [
                        [
                            "go back",
                            "1"
                        ]
                    ]
                }
            ]
        }
    }
    dialog_graph = parse_dialog_from_json(dialog_json)

    assert dialog_graph.current_node().text == "text 1"
    assert dialog_graph.current_node().graphics.image_ids == ["image 1"]
    assert [c.text for c in dialog_graph.current_node().choices] == ["stay here", "go next"]
    dialog_graph.make_choice(1)
    assert dialog_graph.current_node().text == "text 2"
    assert dialog_graph.current_node().graphics.image_ids == ["image 2"]
    assert [c.text for c in dialog_graph.current_node().choices] == ["go back"]


def test_load_graph_with_animation():
    dialog_json = {
        "graph": {
            "root": "1",
            "nodes": [
                {
                    "id": "1",
                    "text": "text 1",
                    "graphics": {
                        "animation": "animation 1",
                    },
                    "choices": []
                }
            ]
        }
    }
    dialog_graph = parse_dialog_from_json(dialog_json)

    assert dialog_graph.current_node().text == "text 1"
    assert dialog_graph.current_node().graphics.animation_id == "animation 1"
    assert dialog_graph.current_node().choices == []
