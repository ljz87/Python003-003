from abc import ABCMeta, abstractclassmethod
import sys

class Zoo(object):

    animals = {}

    def __init__(self, name):
        # 动物园名字
        self.name = name

    @classmethod
    def add_animal(cls, animal):
        if animal not in cls.animals:
            cls.animals[animal] = animal
    
        if not hasattr(cls, animal.__class__.__name__):
            setattr(cls, animal.__class__.__name__, animal)



class Animal(metaclass=ABCMeta):

    @abstractclassmethod
    def __init__(self, genre, physique, character):
        self.genre = genre
        self.physique = physique
        self.character = character

    @property
    def is_fierce_creatures(self):
        return (self.physique == '中型' or self.physique == '大型') and self.genre == '食肉' and self.character == '凶猛'

    @property
    def as_pets(self):
        return (self.physique != '凶猛') 

class Cat(Animal):

    sound = '喵'
    
    def __init__(self, name,genre,physique,character):
        # 动物名字
        self.name = name
        super().__init__(genre, physique, character)

class Dog(Animal):

    sound = 'WoWo'

    def __init__(self, name,genre,physique,character):
        # 动物名字
        self.name = name
        super().__init__(genre, physique, character)

    

if __name__ == '__main__':
    # 实例化动物园
    z = Zoo('时间动物园')
    # 实例化一只猫，属性包括名字、类型、体型、性格
    cat1 = Cat('大花猫 1', '食肉', '小', '温顺')
    # 增加一只猫到动物园
    z.add_animal(cat1)
    # 动物园是否有猫这种动物
    have_cat = hasattr(z, 'Dog')
    print(have_cat)