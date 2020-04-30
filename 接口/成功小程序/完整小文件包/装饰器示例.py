import time

def timer(parameter):

    def outer_wrapper(func):

        def wrapper(*args, **kwargs):
            if parameter == 'task1':
                start = time.time()
                func(*args, **kwargs)
                stop = time.time()
                print("the task1 run time is :", stop - start)
            elif parameter == 'task2':
                start = time.time()
                func(*args, **kwargs)
                stop = time.time()
                print("the task2 run time is :", stop - start)

        return wrapper

    return outer_wrapper

@timer(parameter='task1')
def task1():
    time.sleep(2)
    print("in the task1")

@timer(parameter='task2')
def task2():
    time.sleep(2)
    print("in the task2")

task1()
task2()
#·················································································

import functools
def use_logging(arg):
  if callable(arg):#判断参入的参数是否是函数，不带参数的装饰器调用这个分支
    @functools.wraps(arg)
    def _deco(*args,**kwargs):
      print("%s is running" % arg.__name__)
      arg(*args,**kwargs)
    return _deco
  else:#带参数的装饰器调用这个分支
    def _deco(func):
      @functools.wraps(func)
      def __deco(*args, **kwargs):
        if arg == "warn":
          print("aa%s is running" % func.__name__)
        return func(*args, **kwargs)
      return __deco
    return _deco
@use_logging("warn")
# @use_logging
def bar():
  print('i am bar')
  print(bar.__name__)
bar()
