# hashkey 생성
import hashlib

name = 'example_0624.avi'
id = 1

key = hashlib.sha256()
key.update(name.encode('utf-8'))
key.update(str(id).encode('utf-8'))

print(key)
print(key.digest())
