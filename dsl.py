from pipeline import Pipeline, Node
from typing import List, Dict, Callable


class PipelineDSL:
    """DSL для создания конвейеров."""
    def __init__(self):
        self.pipeline = Pipeline()

    def create_channel(self, name: str, data_type: type):
        return self.pipeline.create_channel(name, data_type)

    def create_node(self, name: str, inputs: Dict[str, str], outputs: Dict[str, str], func: Callable):
        return self.pipeline.create_node(name, inputs, outputs, func)

    def run(self):
        self.pipeline.run()

    def check_status(self):
        """Проверка состояния конвейера."""
        return self.pipeline.check_pipeline_status()
