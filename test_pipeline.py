#Обновлённый test_pipeline
import unittest
from pipeline import Node, Channel, Pipeline, select_best_result


def add_numbers(input_data, params):
    """Функция сложения чисел."""
    return {"result": input_data["a"] + input_data["b"]}


def uppercase_string(input_data, params):
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

    def test_select_best_result(self):
        # Создаем каналы
        result_channel = Channel("results", list)
        best_result_channel = Channel("best_result", dict)

        # Создаем узел
        node = Node(
            name="SelectBestResultNode",
            inputs={"results": result_channel},
            outputs={"best_result": best_result_channel},
            func=select_best_result
        )

        # Отправляем список вариантов
        result_channel.send([
            {"score": 10, "value": "image1.jpg"},
            {"score": 20, "value": "image2.jpg"},
            {"score": 15, "value": "image3.jpg"}
        ])

        # Запускаем узел
        node.process()

        # Проверяем результат
        best_result = best_result_channel.receive()
        self.assertEqual(best_result["value"], "image2.jpg")

    def test_pipeline_cycle_detection(self):
        # Создаем каналы
        a_channel = Channel("a", int)
        b_channel = Channel("b", int)
        result_channel = Channel("result", int)

        # Создаем узлы
        node1 = Node(
            name="Node1",
            inputs={"a": a_channel},
            outputs={"result": result_channel},
            func=add_numbers
        )

        node2 = Node(
            name="Node2",
            inputs={"result": result_channel},
            outputs={"b": b_channel},
            func=add_numbers
        )

        # Создаем цикл в конвейере
        pipeline = Pipeline([node1, node2])

        # Проверка на зацикливание
        with self.assertRaises(ValueError):
            pipeline.run()

    def test_node_update_params(self):
        # Создаем каналы
        a_channel = Channel("a", int)
        b_channel = Channel("b", int)
        result_channel = Channel("result", int)

        # Создаем узел
        node = Node(
            name="AdditionNode",
            inputs={"a": a_channel, "b": b_channel},
            outputs={"result": result_channel},
            func=add_numbers,
            params={"factor": 2}
        )

        # Обновляем параметры узла
        node.update_params({"factor": 3})

        # Проверяем обновление параметров
        self.assertEqual(node.params["factor"], 3)


if __name__ == "__main__":
    unittest.main()
