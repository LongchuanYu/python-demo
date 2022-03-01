import threading
import time

name = 'ly'

def show():
    global name
    time.sleep(2)
    name = 'aa'

thread = threading.Thread(target=show)
thread.daemon = True
thread.start()


while True:
    print(name)
    time.sleep(2)
