from abc import ABCMeta, abstractclassmethod
import sys

class Zoo(object):

    def __init__(self, name):
        # 动物园名字
        self.name = name

    def __getattr__(self, item):
        if sys._getframe().f_back.f_lineno < 37 :
            print(f'__getattr__ called item:{item}')
            setattr(self,item,[])
            return item

    def add_animal(self, animal):
        if animal.__class__.__name__ == 'Cat':
            flag = 0
            for i in self.Cat:
                if id(i) == id(animal) :
                    flag = 1

            if flag != 1 :
                self.Cat.append(animal)
            
        
        if animal.__class__.__name__ == 'Dog':
            print('Dog')
            flag = 0
            for i in self.Dog:
                if id(i) == id(animal) :
                    flag = 1

            if flag != 1 :
                self.Dog.append(animal)



class Animal(metaclass=ABCMeta):
    genre = ''
    physique = ''
    character = ''
    fierce_creatures =''

    @abstractclassmethod
    def is_fierce_creatures(self):
        pass

class Cat(Animal):
    
    def __init__(self, name,genre,physique,character):
        # 动物名字
        self.name = name
        self.genre = genre
        self.physique = physique
        self.character = character
        self.sound = '喵'

        if self.physique == '凶猛' :
            self.forpet = '不适合'
        else :
            self.forpet = '适合'

        self.is_fierce_creatures()


    def is_fierce_creatures(self):
        if self.physique == '肉食' or self.character == '凶猛' :
            self.fierce_creatures = '是'
        else :
            self.fierce_creatures = '否'

class Dog(Animal):

    def __init__(self, name,genre,physique,character):
        # 动物名字
        self.name = name
        self.genre = genre
        self.physique = physique
        self.character = character
        self.sound = 'wowo'

        if self.physique == '凶猛' :
            self.forpet = '不适合'
        else :
            self.forpet = '适合'

        self.is_fierce_creatures()


    def is_fierce_creatures(self):
        if self.physique == '肉食' or self.character == '凶猛' :
            self.fierce_creatures = '是'
        else :
            self.fierce_creatures = '否'

    

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