import io
import mimetypes
import uuid
from pathlib import Path


class Image:
    def __init__(self, config, image_handler):
        self.config = config
        self.image_handler = image_handler

    def on_get(self, req, resp):
        """
        get an image resource

        returns an image with a specified ID
        """
        doc = {
            "name": "test",
            "size": 1024,
            "type": "image/png"
        }
        resp.media = doc

    def on_post(self, req, resp):
        image_details = self.image_handler.save(req.stream, req.content_type)


class ImageHandler:
    _CHUNK_SIZE_BYTES = 4096

    def __init__(self, base_out_path: [str, Path], uuidgen=uuid.uuid4, fopen=io.open):
        self.root: Path = Path(base_out_path)
        self._uuidgen = uuidgen
        self._fopen = fopen

    def save(self, image_stream, image_content_type, orig_image_name) -> dict:
        ext = mimetypes.guess_extension(image_content_type)
        im_type = ext.replace(".", "")
        image_uuid = self._uuidgen()
        name = f"{image_uuid}{ext}"
        image_path = self.root / name
        size = 0
        with self._fopen(image_path, "wb") as image_file:
            chunk = image_stream.read(self._CHUNK_SIZE_BYTES)
            size += len(chunk)
            while chunk is not None:
                image_file.write(chunk)

        return dict(
            original_name=orig_image_name,
            type=im_type,
            uuid=image_uuid,
            path=str(image_path),
            size=size
        )

    def load(self, path: [str, Path]):
        with self._fopen(path, "rb") as image_file:
            img_bytes = image_file.read()

        return  img_bytes