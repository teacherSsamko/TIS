"""
How to update console output2 (for python version 3.x)

line you need to add \r (​character return) and end="" 
so that you do not go to the next line. Carriage return 
or \r is a very unique feature of Python. 
\r will just work as you have shifted your cursor to the beginning of the string or line. 
Whenever you will use this special escape character \r, 
the rest of the content after the \r will come at the front of your line 
and will keep replacing your characters one by one until it takes all the contents
left after the \r in that string. How does Carriage Return \r work in Python. 
"""
import time


for i in range(10):
    print(f'\rDoing thing {i}', end='')
    time.sleep(1)