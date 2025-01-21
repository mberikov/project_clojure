# pipeline.py

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

    def start(self):
        """Запуск узла в отдельном потоке."""
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self):
        while True:
            try:
                self.process()
            except Empty:
                continue
