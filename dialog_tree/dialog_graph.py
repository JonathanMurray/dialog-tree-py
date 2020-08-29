from typing import List, Optional, Dict


class DialogChoice:
    def __init__(self, text: str, leads_to_id: str):
        self.text = text
        self.leads_to_id = leads_to_id


class DialogNode:
    def __init__(self, node_id: str, text: str, animation_image_ids: List[str], choices: List[DialogChoice]):
        if not node_id or not text:
            raise ValueError("Invalid node config")
        self.node_id = node_id
        self.text = text
        self.animation_image_ids = animation_image_ids
        self.choices = choices


class DialogGraph:
    def __init__(self, root_id: str, nodes: List[DialogNode], title: Optional[str] = None):
        self.title = title
        self._nodes_by_id: Dict[str, DialogNode] = {}
        self._active_node_id = root_id
        for node in nodes:
            node_id = node.node_id
            if node_id in self._nodes_by_id:
                raise ValueError(f"Duplicate node ID found: {node_id}")
            self._nodes_by_id[node_id] = node

        for node in nodes:
            for choice in node.choices:
                if choice.leads_to_id not in self._nodes_by_id:
                    raise ValueError(
                        f"Dialog choice leading to missing node: {choice.leads_to_id}")

        if root_id not in self._nodes_by_id:
            raise ValueError(f"No node found with ID: {root_id}")

    def current_node(self) -> DialogNode:
        return self._nodes_by_id[self._active_node_id]

    def make_choice(self, choice_index: int):
        node = self._nodes_by_id[self._active_node_id]
        self._active_node_id = node.choices[choice_index].leads_to_id

    def nodes(self) -> List[DialogNode]:
        """ Return the nodes of this graph as a list. Should not needed for normal usage,
         but is used when visualizing the graph with graphviz. """
        return list(self._nodes_by_id.values())

    def __repr__(self):
        return str(self.__dict__)
