import shortid


sid = shortid.ShortId()
for i in range(10):
    key = sid.generate()
    print(key, ' : ', len(key))