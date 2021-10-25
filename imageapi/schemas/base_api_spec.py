from spectree import Response, SpecTree, Tag


def before_handler(req, resp, err, instance):
    if err:
        print(req)
        print(resp)
        print(err)
        resp.set_header("X-Error", "Validation Error")


def after_handler(req, resp, err, instance):
    resp.set_header("X-Name", instance)
    if err:
        print(err)
        print(resp)
        print(req)



api = SpecTree(
    "falcon",
    title="Image Tagging API for annalise.ai",
    version="0.0.1",
    openapi="3.0.0",
    annotations=True,
    before=before_handler,
    after=after_handler
)
