import pytest

from dialog_config_file import parse_dialog_from_json


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

    assert dialog_graph.get_current_state() == ("text 1", "image 1", ["Next"])
    dialog_graph.make_choice(0)
    assert dialog_graph.get_current_state() == ("text 2", "image 2", ["Play from beginning"])


def test_load_graph():
    dialog_json = {
        "graph": {
            "root": "1",
            "nodes": [
                {
                    "id": "1",
                    "text": "text 1",
                    "image": "image 1",
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
                    "image": "image 2",
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

    assert dialog_graph.get_current_state() == ("text 1", "image 1", ["stay here", "go next"])
    dialog_graph.make_choice(1)
    assert dialog_graph.get_current_state() == ("text 2", "image 2", ["go back"])
