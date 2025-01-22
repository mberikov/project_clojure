from typing import Dict, Callable
from pipeline import Channel, Node

def create_channel(name: str, data_type: type) -> Channel:
    """Создает канал с типизацией."""
    return Channel(name, data_type)


def create_node(name: str, inputs: Dict[str, Channel], outputs: Dict[str, Channel], func: Callable) -> Node:
    """Создает узел."""
    return Node(name, inputs, outputs, func)
