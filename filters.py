# filters.py
from typing import Dict, Any
from typing import Dict


def blur(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Симуляция фильтра Blur."""
    image = input_data["image"]
    return {"image": f"{image} [Blur applied]"}


def convert_png_to_jpg(input_data: Dict[str, Any]) -> Dict[str, Any]:
    
    """Симуляция преобразования PNG -> JPG."""
    image = input_data["image"]
    return {"image": image.replace(".png", ".jpg")}


def merge_images(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Симуляция сшивки панорамы."""
    images = input_data["images"]
    return {"panorama": " + ".join(images)}


def split_image(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Симуляция разрезания изображения."""
    image = input_data["image"]
    return {"part1": f"{image} [part1]", "part2": f"{image} [part2]"}
