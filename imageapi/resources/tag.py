class Tag:
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

    def on_post(self):
        pass

