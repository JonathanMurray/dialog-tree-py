import json
from typing import List, Dict

from constants import Millis
from graph import DialogGraph, DialogNode, DialogChoice, NodeGraphics


def load_dialog_from_file(file_path: str) -> DialogGraph:
    print(f"Loading dialog: {file_path}")
    with open(file_path) as f:
        return parse_dialog_from_json(json.load(f))


def parse_dialog_from_json(dialog_json: Dict) -> DialogGraph:
    if "graph" in dialog_json:
        dialog_graph = _parse_graph_json(dialog_json["graph"])
    elif "sequence" in dialog_json:
        dialog_graph = _parse_sequence_json(dialog_json["sequence"])
    else:
        raise ValueError(f"Invalid configuration file!")

    dialog_graph.title = dialog_json.get("title", None)
    dialog_graph.background_image_id = dialog_json.get("background_image_id", None)
    return dialog_graph


def _parse_sequence_json(sequence_json) -> DialogGraph:
    root_id = "START"
    initial_step = sequence_json[0]
    next_text = "Next"
    nodes = [
        DialogNode(root_id, initial_step[0], NodeGraphics(image_ids=[initial_step[1]]),
                   [DialogChoice(next_text, "1")])]
    for i in range(1, len(sequence_json) - 1):
        step = sequence_json[i]
        nodes.append(
            DialogNode(str(i), step[0], NodeGraphics(image_ids=[step[1]]), [DialogChoice(next_text, str(i + 1))]))
    last_step = sequence_json[-1]
    nodes.append(
        DialogNode(str(len(sequence_json) - 1), last_step[0], NodeGraphics(image_ids=[last_step[1]]),
                   [DialogChoice("Play from beginning", root_id)]))
    return DialogGraph(root_id, nodes)


def _parse_graph_json(graph_json) -> DialogGraph:
    def parse_choice(array: List[str]) -> DialogChoice:
        return DialogChoice(array[0], array[1])

    def parse_node(node) -> DialogNode:
        graphics = node["graphics"]
        offset = graphics.get("offset", None)
        screen_shake = Millis(graphics["screen_shake"]) if "screen_shake" in graphics else None
        instant_text = graphics.get("instant_text", False)
        if "image" in graphics:
            node_graphics = NodeGraphics(image_ids=[graphics["image"]], offset=offset, screen_shake=screen_shake,
                                         instant_text=instant_text)
        elif "animation" in graphics:
            node_graphics = NodeGraphics(animation_id=graphics["animation"], offset=offset,
                                         screen_shake=screen_shake, instant_text=instant_text)
        else:
            raise ValueError(f"Missing image/animation config for node!")
        return DialogNode(
            node_id=node["id"],
            text=node["text"],
            graphics=node_graphics,
            choices=[parse_choice(choice) for choice in node["choices"]],
            sound_id=node.get("sound", None))

    return DialogGraph(graph_json["root"], [parse_node(node) for node in graph_json["nodes"]])
