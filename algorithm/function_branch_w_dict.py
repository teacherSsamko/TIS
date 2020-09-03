def hello():
    print("hello")

def world():
    print("world")

action = "h"

functions = dict(h=hello, w=world)
functions[action]()
