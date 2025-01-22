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
    def __init__(self, name: str, inputs: Dict[str, Channel], outputs: Dict[str, Channel], func: Callable):
        self.name = name
        self.inputs = inputs
        self.outputs = outputs
        self.func = func
        self.lock = threading.Lock()
        self.is_active = True  # Состояние узла

    def process(self):
        """Основная логика обработки данных."""
        with self.lock:
            try:
                # Получаем данные из входных каналов
                input_data = {name: channel.receive() for name, channel in self.inputs.items()}
                
                # Выполняем функцию обработки
                output_data = self.func(input_data)

                # Отправляем результат в выходные каналы
                if isinstance(output_data, dict):
                    for name, data in output_data.items():
                        if name in self.outputs:
                            self.outputs[name].send(data)

            except Exception as e:
                logging.error(f"Error in node '{self.name}': {e}")
                self.is_active = False  # Узел завершил работу из-за ошибки

    def start(self):
        """Запуск узла в отдельном потоке."""
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self):
        while self.is_active:
            try:
                self.process()
            except Empty:
                continue


class Pipeline:
    """Конвейер обработки данных с поддержкой циклов."""
    def __init__(self):
        self.nodes = []
        self.channels = {}
        self.max_iterations = 10  # максимальное количество итераций

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
        iteration = 0
        while iteration < self.max_iterations:
            if not self.check_pipeline_status():
                break
            for node in self.nodes:
                node.start()
            iteration += 1
            logging.info(f"Итерация {iteration} завершена.")
            
            # Диагностика на случай бесконечного цикла
            if iteration >= self.max_iterations:
                logging.error("Конвейер зашел в бесконечный цикл!")
                break

    def check_pipeline_status(self):
        """Проверка статуса конвейера (активность всех узлов)."""
        return all(node.is_active for node in self.nodes)
