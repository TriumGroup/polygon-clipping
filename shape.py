from abc import abstractclassmethod


class Shape:
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
