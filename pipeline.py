#обновленный pipeline
import threading
from queue import Queue, Empty
from typing import Callable, List, Any, Dict, Tuple
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


class Channel:
    """Канал для передачи данных между узлами."""
    def __init__(self, name: str, data_type: type):
        self.name = name
        self.data_type = data_type
        self.queue = Queue()

    def send(self, data: Any):
        if not isinstance(data, self.data_type):
            raise TypeError(f"Invalid data type for channel {self.name}: {type(data)}")
        self.queue.put(data)

    def receive(self) -> Any:
        return self.queue.get()


class Node:
    """Узел конвейера."""
    def __init__(self, name: str, inputs: Dict[str, Channel], outputs: Dict[str, Channel], func: Callable, params: Dict[str, Any] = None):
        self.name = name
        self.inputs = inputs
        self.outputs = outputs
        self.func = func
        self.params = params if params else {}
        self.lock = threading.Lock()
        self.finished = False  # Признак завершения работы узла

    def process(self):
        """Основная логика обработки данных."""
        with self.lock:
            try:
                # Получаем данные из входных каналов
                input_data = {name: channel.receive() for name, channel in self.inputs.items()}
                
                # Выполняем функцию обработки
                output_data = self.func(input_data, self.params)

                # Отправляем результат в выходные каналы
                if isinstance(output_data, dict):
                    for name, data in output_data.items():
                        if name in self.outputs:
                            self.outputs[name].send(data)

                # Устанавливаем флаг завершения работы
                self.finished = True

            except Exception as e:
                logging.error(f"Error in node '{self.name}': {e}")

    def start(self):
        """Запуск узла в отдельном потоке."""
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self):
        while not self.finished:
            try:
                self.process()
            except Empty:
                continue

    def update_params(self, new_params: Dict[str, Any]):
        """Обновление параметров узла во время работы конвейера."""
        self.params.update(new_params)
        logging.info(f"Updated parameters for node '{self.name}': {self.params}")


class Pipeline:
    """Конвейер обработки данных, состоящий из связанных узлов."""
    def __init__(self, nodes: List[Node]):
        self.nodes = nodes
        self.visited_nodes = set()

    def run(self):
        """Запуск конвейера и обработка данных."""
        for node in self.nodes:
            if node.name not in self.visited_nodes:
                self.visited_nodes.add(node.name)
                node.start()
            else:
                raise ValueError(f"Cyclic dependency detected in node '{node.name}'")

        # Проверяем, завершена ли работа всех узлов
        while not all(node.finished for node in self.nodes):
            pass


def select_best_result(input_data, params):
    """Функция для выбора лучшего результата из нескольких вариантов."""
    # Входные данные будут представлять собой список вариантов
    results = input_data["results"]
    # Пример: выбираем вариант с наибольшим числовым значением
    best_result = max(results, key=lambda x: x["score"])
    return {"best_result": best_result}


