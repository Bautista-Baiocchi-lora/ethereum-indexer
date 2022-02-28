from interfaces.itransform import ITransform


class Transform(ITransform):
    def __init__(self):
        ...

    def _validate_transformers(self) -> None:
        ...

    def transform(self) -> None:
        ...

    def flush(self) -> None:
        ...
