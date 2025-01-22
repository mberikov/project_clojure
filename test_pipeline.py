import unittest
from pipeline import Node, Channel


def add_numbers(input_data):
    """Функция сложения чисел."""
    return {"result": input_data["a"] + input_data["b"]}


def uppercase_string(input_data):
    """Функция преобразования строки в верхний регистр."""
    return {"output": input_data["input"].upper()}


class TestPipeline(unittest.TestCase):
    def test_add_numbers(self):
        # Создаем каналы
        a_channel = Channel("a", int)
        b_channel = Channel("b", int)
        result_channel = Channel("result", int)

        # Создаем узел
        node = Node(
            name="AdditionNode",
            inputs={"a": a_channel, "b": b_channel},
            outputs={"result": result_channel},
            func=add_numbers
        )

        # Отправляем данные
        a_channel.send(3)
        b_channel.send(7)

        # Запускаем узел
        node.process()

        # Проверяем результат
        result = result_channel.receive()
        self.assertEqual(result, 10)

    def test_uppercase_string(self):
        # Создаем каналы
        input_channel = Channel("input", str)
        output_channel = Channel("output", str)

        # Создаем узел
        node = Node(
            name="UppercaseNode",
            inputs={"input": input_channel},
            outputs={"output": output_channel},
            func=uppercase_string
        )

        # Отправляем данные
        input_channel.send("hello")

        # Запускаем узел
        node.process()

        # Проверяем результат
        result = output_channel.receive()
        self.assertEqual(result, "HELLO")

    def test_error_handling(self):
        def faulty_function(input_data):
            raise ValueError("Intentional error")

        # Создаем каналы
        input_channel = Channel("input", int)
        output_channel = Channel("output", int)

        # Создаем узел
        node = Node(
            name="FaultyNode",
            inputs={"input": input_channel},
            outputs={"output": output_channel},
            func=faulty_function
        )

        # Отправляем данные
        input_channel.send(42)

        # Запускаем узел
        with self.assertLogs(level="ERROR") as log:
            node.process()
            self.assertIn("Error in node 'FaultyNode'", log.output[0])


if __name__ == "__main__":
    unittest.main()
