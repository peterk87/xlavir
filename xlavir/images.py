import logging
from pathlib import Path
from typing import List, Optional

from xlavir.util import list_get


class SheetImage(object):
    def __init__(self, image_path: Path, sheet_name: str, image_description: str):
        self.image_path = image_path
        self.sheet_name = sheet_name
        self.image_description = image_description


def get_images_for_sheets(image: List[Path],
                          image_title: Optional[List[str]],
                          image_description: Optional[List[str]]) -> List[SheetImage]:
    out = []
    for i, img in enumerate(image):
        title: str = list_get(image_title[0:31], i, img.stem[0:31])
        desc: str = list_get(image_description, i, f'Image from "{img.name}"')
        logging.debug(f'{i}: {title} | {desc} | {img}')
        out.append(SheetImage(image_path=img,
                              sheet_name=title,
                              image_description=desc))
    return out
