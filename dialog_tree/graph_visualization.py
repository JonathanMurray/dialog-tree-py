#!/usr/bin/env python3
import os
import sys
from pathlib import Path

from graphviz import Digraph

from constants import DIALOG_DIR
from dialog_config_file import load_dialog_from_file
from graph import DialogGraph
from text_util import layout_text_in_area

TMP_DIR = Path(".tmpfiles")


def generate_graphviz(graph_name: str, dialog_graph: DialogGraph) -> Digraph:
    graph = Digraph(
        name=graph_name,
        comment=f"generated with Graphviz from {graph_name}",
        node_attr={"shape": "box", "style": "filled", "color": "#BBCCFF"},
        edge_attr={"fontsize": "11"}
    )
    for node in dialog_graph.nodes():
        node_label = _add_newlines(node.text, 30)
        graph.node(node.node_id, node_label)
        for choice in node.choices:
            edge_label = _add_newlines(choice.text, 20)
            graph.edge(node.node_id, choice.leads_to_id, label=edge_label)
    return graph


def _add_newlines(text: str, max_chars_per_line: int) -> str:
    lines_iterator = layout_text_in_area(text, len, max_chars_per_line)
    text_with_newlines = next(lines_iterator)
    for additional_line in lines_iterator:
        text_with_newlines += f"\n{additional_line}"
    return text_with_newlines


def _init_tmp_dir():
    if not TMP_DIR.exists():
        print(f"Creating directory: {TMP_DIR}")
        os.mkdir(TMP_DIR)
    for existing_file in [TMP_DIR.joinpath(f) for f in os.listdir(TMP_DIR)]:
        print(f"Cleaning up old file: {existing_file}")
        os.remove(existing_file)


def main():
    args = sys.argv[1:]
    dialog_filename = args[0] if args else "wikipedia_example.json"
    dialog_graph = load_dialog_from_file(f"{DIALOG_DIR}/{dialog_filename}")
    _init_tmp_dir()
    graph = generate_graphviz(dialog_filename, dialog_graph)
    graph.render(directory=TMP_DIR, view=True)
    print(f"Saved rendered outputs in: {TMP_DIR}")


if __name__ == '__main__':
    main()
