i = 0
while i < 10:
    try:
        i += 1
        print(i)
        pass
    finally:
        i += 2
        print(i) 