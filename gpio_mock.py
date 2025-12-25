class GaletteMock:
    def __init__(self):
        self.position = 1

    def set_position(self, pos: int):
        if 1 <= pos <= 11:
            self.position = pos

    def get_position(self) -> int:
        return self.position
