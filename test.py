# def Singleton(cls):
#     _instance = {}

#     def _singleton(*args, **kwargs):
#         if cls not in _instance:
#             _instance[cls] = cls(*args, **kwargs)
#         return _instance[cls]
#     return _singleton


# class Test(object):
#     def __init__(self, a) -> None:
#         self.a = a


# singleton = Singleton(Test)
# instance1 = singleton('instance1')
# instance2 = singleton('instance2')
# print(id(instance1))
# print(id(instance2))



import signal
import time

def test(*args):
    print('closed', time.time())



signal.signal(signal.SIGTERM, test)
signal.signal(signal.SIGINT, test)
signal.signal(signal.SIGTSTP, test)


while 1:
    time.sleep(1)