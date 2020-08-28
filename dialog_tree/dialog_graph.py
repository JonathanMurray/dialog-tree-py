from typing import List, Tuple, Optional


class DialogChoice:
    def __init__(self, text: str, leads_to_id: str):
        self.text = text
        self.leads_to_id = leads_to_id


class DialogNode:
    def __init__(self, node_id: str, text: str, image_id: str, choices: List[DialogChoice]):
        if not node_id or not text:
            raise ValueError("Invalid node config")
        self.node_id = node_id
        self.text = text
        self.image_id = image_id
        self.choices = choices


class DialogGraph:
    def __init__(self, root_id: str, nodes: List[DialogNode], title: Optional[str] = None):
        self.title = title
        self._nodes_by_id = {}
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

    def get_current_state(self) -> Tuple[str, str, List[str]]:
        """Get dialog text, image ID and a list of choices"""
        node = self._nodes_by_id[self._active_node_id]
        return node.text, node.image_id, [c.text for c in node.choices]

    def make_choice(self, choice_index: int):
        node = self._nodes_by_id[self._active_node_id]
        self._active_node_id = node.choices[choice_index].leads_to_id

    def __repr__(self):
        return str(self.__dict__)
