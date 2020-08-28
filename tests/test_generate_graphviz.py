from dialog_graph import DialogGraph, DialogNode, DialogChoice
from graph_visualization import generate_graphviz


def test_simple_graphviz():
    dialog_graph = DialogGraph(
        root_id="ROOT_NODE",
        nodes=[DialogNode("ROOT_NODE", "Start text", "some_image.png", [DialogChoice("Choice text", "OTHER_NODE")]),
               DialogNode("OTHER_NODE", "Other text", "other_image.png", [])]
    )

    graph = generate_graphviz("Some name", dialog_graph)

    assert graph.name == "Some name"
    assert set(graph.body) == {
        '\tROOT_NODE [label="Start text"]',
        '\tROOT_NODE -> OTHER_NODE [label="Choice text"]',
        '\tOTHER_NODE [label="Other text"]'
    }
