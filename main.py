from dsl import PipelineDSL
from filters import blur, convert_png_to_jpg, merge_images, split_image

def main():
    pipeline = PipelineDSL()

    # Создание каналов
    input_channel = pipeline.create_channel("input", str)
    blur_channel = pipeline.create_channel("blur", str)
    jpg_channel = pipeline.create_channel("jpg", str)
    panorama_channel = pipeline.create_channel("panorama", str)

    # Создание узлов
    pipeline.create_node("BlurNode", {"image": "input"}, {"image": "blur"}, blur)
    pipeline.create_node("ConvertNode", {"image": "blur"}, {"image": "jpg"}, convert_png_to_jpg)
    pipeline.create_node("MergeNode", {"images": "jpg"}, {"panorama": "panorama"}, merge_images)

    # Запуск конвейера
    pipeline.run()

    # Отправка данных
    input_channel.send("image1.png")
    input_channel.send("image2.png")


if __name__ == "__main__":
    main()
