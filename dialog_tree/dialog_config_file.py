import json
from typing import List, Dict

from dialog_graph import DialogGraph, DialogNode, DialogChoice, AnimationRef


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
    return dialog_graph


def _parse_sequence_json(sequence_json) -> DialogGraph:
    root_id = "START"
    initial_step = sequence_json[0]
    next_text = "Next"
    nodes = [
        DialogNode(root_id, initial_step[0], AnimationRef.of_image_ids([initial_step[1]]),
                   [DialogChoice(next_text, "1")])]
    for i in range(1, len(sequence_json) - 1):
        step = sequence_json[i]
        nodes.append(
            DialogNode(str(i), step[0], AnimationRef.of_image_ids([step[1]]), [DialogChoice(next_text, str(i + 1))]))
    last_step = sequence_json[-1]
    nodes.append(
        DialogNode(str(len(sequence_json) - 1), last_step[0], AnimationRef.of_image_ids([last_step[1]]),
                   [DialogChoice("Play from beginning", root_id)]))
    return DialogGraph(root_id, nodes)


def _parse_graph_json(graph_json) -> DialogGraph:
    def parse_choice(array: List[str]) -> DialogChoice:
        return DialogChoice(array[0], array[1])

    def parse_node(node) -> DialogNode:
        if "image" in node:
            animation_ref = AnimationRef.of_image_ids([node["image"]])
        elif "animation" in node:
            animation_ref = AnimationRef.of_image_ids(node["animation"])
        elif "animation_dir" in node:
            animation_ref = AnimationRef.of_directory(node["animation_dir"])
        else:
            raise ValueError(f"Missing image/animation config for node!")
        return DialogNode(
            node_id=node["id"],
            text=node["text"],
            animation_ref=animation_ref,
            choices=[parse_choice(choice) for choice in node["choices"]])

    return DialogGraph(graph_json["root"], [parse_node(node) for node in graph_json["nodes"]])
