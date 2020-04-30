'''
class Student(object):
    # __init__是一个特殊方法用于在创建对象时进行初始化操作
    # 通过这个方法我们可以为学生对象绑定name和age两个属性
    def __init__(self,name,age):
        self.name=name
        self.age=age
    def study(self,course_name):
        print('%s正在学习%s.'%(self.name,course_name))
    # PEP 8要求标识符的名字用全小写多个单词用下划线连接
    # 但是部分程序员和公司更倾向于使用驼峰命名法(驼峰标识)
    def watch_movie(self):
        if self.age<18:
            print("%s只能观看《熊出没》."%self.name)
        else:
            print('%s正在观看金刚葫芦.'%self.name)
def main():
    # 创建学生对象并指定姓名和年龄
    stu1=Student('骆昊',38)
    # 给对象发study消息
    stu1.study('Python程序设计')
    # 给对象发watch_av消息
    stu1.watch_movie()
    stu2=Student('王大锤',15)
    stu2.study('思想品德')
    stu2.watch_movie()
if __name__=='__main__':
    main()'''
'''
class Test:
    def __init(self,foo):
        self._foo=foo
    def _bar(self):
        print(self._foo)
        print('_bar')
def main():
    test=Test('hello')
    # AttributeError: 'Test' object has no attribute '__bar'
    test._bar()
    # AttributeError: 'Test' object has no attribute '__foo'
    print(test._foo)
if __name__=='__main__':
    main()'''
'''
from time import sleep
class Clock(object):
    "数字时钟"
    def __init__(self,hour=0,minute=0,second=0):
        """初始化方法
        :param hour: 时
        :param minute: 分
        :param second: 秒
        """
        self._hour=hour
        self._minute=minute
        self._second=second
    def run(self):
        """走字"""
        self._second+=1
        if self._second==60:
            self._second=0
            self._minute+=1
            if self._minute==60:
                self._minute=0
                self._hour+=1
                if self._hour==24:
                    self._hour=0
    def show(self):
        """显示时间"""
        return '%02d:%02d:%02d'%\
               (self._hour,self._minute,self._second)
def main():
    clock=Clock(23,59,58)
    while True:
        print(clock.show())
        sleep(1)
        clock.run()
if __name__ == '__main__':
    main()'''
'''
from math import sqrt
class Point(object):
    def __init__(self,x=0,y=0):
        """初始化方法

        :param x: 横坐标
        :param y: 纵坐标
        """
        self.x=x
        self.y=y
    def move_to(self,x,y):
        """移动到指定位置

        :param x: 新的横坐标
        param y: 新的纵坐标
        """
        self.x = x
        self.y = y
    def move_by(self,dx,dy):
        """移动指定的增量

        :param dx: 横坐标的增量
        param dy: 纵坐标的增量
        """
        self.x+=dx
        self.y+=dy
    def distance_to(self,other):
        """计算与另一个点的距离

         :param other: 另一个点
         """
        dx=self.x-other.x
        dy=self.y-other.y
        return sqrt(dx**2+dy**2)
    def __str__(self):
        return '(%s,%s)'%(str(self.x),str(self.y))
def main():
    p1=Point(3,5)
    p2=Point()
    print(p1)
    print(p2)
    p2.move_by(-1,2)
    print(p2)
    print(p1.distance_to(p2))
if __name__=='__main__':
    main()'''
'''
class Person(object):
    def __init__(self,name,age):
        self._name=name
        self._age=age
    # 访问器 - getter方法
    def name(self):
        return self._name
    # 访问器 - getter方法
    def age(self):
        return self._age
    # 修改器 - setter方法
    def age(self,age):
        self._age=age
    def play(self):
        if self._age<=16:
            print('%s正在玩飞行棋.'% self._name)
        else:
            print('%s正在玩斗地主.'% self._name)
def main():
    person=Person('王大锤',12)
    person.play()
    person.age = 22
    person.play()
    # person.name = '白元芳'  # AttributeError: can't set attribute
if __name__=='__main__':
    main()'''
'''
class Person(object):
    # 限定Person对象只能绑定_name, _age和_gender属性
    __slots__ = ('_name','_age','_gender')
    def __init__(self,name,age):
        self._name=name
        self._age=age
    def name(self):
        return self._name
    def age(self):
        return  self._age
    def age(self,age):
        self._age=age

    def play(self):
        if self._age <= 16:
            print('%s正在玩飞行棋.' % self._name)
        else:
            print('%s正在玩斗地主.' % self._name)
def main():
    person = Person('王大锤', 22)
    person.play()
    person._gender = '男'
    # AttributeError: 'Person' object has no attribute '_is_gay'
    # person._is_gay = True
    '''
'''
from math import sqrt
class Triangle(object):
    def __init__(self, a, b, c):
        self._a = a
        self._b = b
        self._c = c
    def is_valid(a, b, c):
        return a + b > c and b + c > a and a + c > b
    def perimeter(self):
        return self._a + self._b + self._c
    def area(self):
        half = self.perimeter() / 2
        return sqrt(half * (half - self._a) *
                    (half - self._b) * (half - self._c))
def main():
    a, b, c = 3, 4, 5
    # 静态方法和类方法都是通过给类发消息来调用的
    if Triangle.is_valid(a, b, c):
        t = Triangle(a, b, c)
        print(t.perimeter())
        # 也可以通过给类发消息来调用对象方法但是要传入接收消息的对象作为参数
        # print(Triangle.perimeter(t))
        print(t.area())
        # print(Triangle.area(t))
    else:
        print('无法构成三角形.')
if __name__ == '__main__':
    main()'''
'''
from time import time, localtime, sleep
class Clock(object):
    """数字时钟"""
    def __init__(self, hour=0, minute=0, second=0):
        self._hour = hour
        self._minute = minute
        self._second = second
    @classmethod
    def now(cls):
        ctime = localtime(time())
        return cls(ctime.tm_hour, ctime.tm_min, ctime.tm_sec)
    def run(self):
        """走字"""
        self._second += 1
        if self._second == 60:
            self._second = 0
            self._minute += 1
            if self._minute == 60:
                self._minute = 0
                self._hour += 1
                if self._hour == 24:
                    self._hour = 0

    def show(self):
        """显示时间"""
        return '%02d:%02d:%02d' % \
               (self._hour, self._minute, self._second)
def main():
    # 通过类方法创建对象并获取系统时间
    clock = Clock.now()
    while True:
        print(clock.show())
        sleep(1)
        clock.run()
if __name__ == '__main__':
    main()'''
'''
class Person(object):
    """人"""
    def __init__(self, name, age):
        self._name = name
        self._age = age
    def name(self):
        return self._name
    def age(self):
        return self._age
    def age(self, age):
        self._age = age
    def play(self):
        print('%s正在愉快的玩耍.' % self._name)
    def watch_av(self):
        if self._age >= 18:
            print('%s正在观看爱情动作片.' % self._name)
        else:
            print('%s只能观看《熊出没》.' % self._name)
class Student(Person):
    """学生"""
    def __init__(self, name, age, grade):
        super().__init__(name, age)
        self._grade = grade
    def grade(self):
        return self._grade
    def grade(self, grade):
        self._grade = grade
    def study(self, course):
        print('%s的%s正在学习%s.' % (self._grade, self._name, course))
class Teacher(Person):
    """老师"""
    def __init__(self, name, age, title):
        super().__init__(name, age)
        self._title = title
    def title(self):
        return self._title
    def title(self, title):
        self._title = title
    def teach(self, course):
        print('%s%s正在讲%s.' % (self._name, self._title, course))
def main():
    stu = Student('王大锤', 15, '初三')
    stu.study('数学')
    stu.watch_av()
    t = Teacher('骆昊', 38, '老叫兽')
    t.teach('Python程序设计')
    t.watch_av()
if __name__ == '__main__':
    main()'''
'''
from abc import ABCMeta, abstractmethod
class Pet(object, metaclass=ABCMeta):
    """宠物"""
    def __init__(self, nickname):
        self._nickname = nickname
    @abstractmethod
    def make_voice(self):
        """发出声音"""
        pass
class Dog(Pet):
    """狗"""
    def make_voice(self):
        print('%s: 汪汪汪...' % self._nickname)
class Cat(Pet):
    """猫"""
    def make_voice(self):
        print('%s: 喵...喵...' % self._nickname)
def main():
    pets = [Dog('旺财'), Cat('凯蒂'), Dog('大黄')]
    for pet in pets:
        pet.make_voice()
if __name__ == '__main__':
    main()'''
