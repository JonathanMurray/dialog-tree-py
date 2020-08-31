from graph import DialogGraph, DialogNode, DialogChoice, NodeGraphics
from graph_visualization import generate_graphviz


def test_simple_graphviz():
    dialog_graph = DialogGraph(
        root_node_id="ROOT_NODE",
        nodes=[DialogNode("ROOT_NODE", "Start text",
                          [DialogChoice("Choice text", "OTHER_NODE")], NodeGraphics(image_ids=["some_image.png"])),
               DialogNode("OTHER_NODE", "Other text", [], NodeGraphics(image_ids=["other_image.png"]))]
    )

    graph = generate_graphviz("Some name", dialog_graph)

    assert graph.name == "Some name"
    assert set(graph.body) == {
        '\tROOT_NODE [label="Start text"]',
        '\tROOT_NODE -> OTHER_NODE [label="Choice text"]',
        '\tOTHER_NODE [label="Other text"]'
    }
