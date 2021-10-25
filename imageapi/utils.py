import io
import mimetypes
import uuid
from pathlib import Path
from typing import Any, Dict

import dynamic_yaml


def load_config(config_path: Path):
    with open(config_path) as conf:
        config = dynamic_yaml.load(conf)
    return config


def check_mode(attribute, dec):
    def _check_authorization(f):
        def wrapper(self, *args):
            mode = getattr(self, attribute)
            if mode != "test":
                return dec(f(self, *args))
            return f(self, *args)

        return wrapper

    return _check_authorization


class ImageHandler:

    def __init__(self, outpath: [str, Path], chunk_size, uuidgen: uuid.uuid4 = uuid.uuid4, fopen: io.open=io.open):
        self.root: Path = Path().cwd() / outpath
        if not self.root.exists():
            self.root.mkdir(exist_ok=True, parents=True)
        self._uuidgen = uuidgen
        self._fopen = fopen
        self.chunk_size = chunk_size

    def save(self, image_stream: io.IOBase, image_content_type: str, orig_image_name:str) -> Dict[str,Any]:
        ext = mimetypes.guess_extension(image_content_type)
        im_type = ext.replace(".", "")
        image_uuid = self._uuidgen()
        name = f"{image_uuid}{ext}"
        image_path = self.root / name

        with self._fopen(image_path, "wb") as image_file:
            chunk = image_stream.read(self.chunk_size)
            size=len(chunk)
            while chunk:
                image_file.write(chunk)
                chunk = image_stream.read(self.chunk_size)
                size += len(chunk)



        return dict(
            name=orig_image_name,
            content_type=image_content_type,
            type=im_type,
            uuid=image_uuid,
            path=str(image_path),
            size=size
        )

    def load(self, path: [str, Path]) -> io.open:

        return self._fopen(path, "rb")

    def delete(self, path: [str, Path]) -> bool:
        file_to_delete = Path(path)
        if file_to_delete.exists():
            file_to_delete.unlink()
            return True

        return False

