class Report:

    def update (self, request: str) -> None:
        raise NotImplementedError()

    def __str__ (self) -> str:
        raise NotImplementedError()
