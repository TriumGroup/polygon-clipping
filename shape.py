from abc import abstractclassmethod


class Shape:
    DEFAULT_DASH_LENGTH = 4
    ALWAYS_VISIBLE = lambda point: True
    PRECISION = 0.0001

    @abstractclassmethod
    def draw(self):
        pass

    @abstractclassmethod
    def rotate(self, angle):
        pass

    @abstractclassmethod
    def move(self, vector):
        pass

    @abstractclassmethod
    def contains(self, point):
        pass
