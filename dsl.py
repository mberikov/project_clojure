from pipeline import Node, Channel
from typing import List, Dict, Callable


class PipelineDSL:
    """DSL для создания конвейеров."""
    def __init__(self):
        self.nodes = []
        self.channels = {}

    def create_channel(self, name: str, data_type: type):
        channel = Channel(name, data_type)
        self.channels[name] = channel
        return channel

    def create_node(self, name: str, inputs: Dict[str, str], outputs: Dict[str, str], func: Callable):
        input_channels = {k: self.channels[v] for k, v in inputs.items()}
        output_channels = {k: self.channels[v] for k, v in outputs.items()}
        node = Node(name, input_channels, output_channels, func)
        self.nodes.append(node)
        return node

    def run(self):
        for node in self.nodes:
            node.start()
