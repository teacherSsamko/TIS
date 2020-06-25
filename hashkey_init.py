# hashkey 생성
from hashlib import blake2b

name = 'example_0624.avi'
id = 1

key = blake2b(digest_size=10)
key.update(name.encode('utf-8'))
key.update(str(id).encode('utf-8'))

print(key)
print(key.digest())
print(key.hexdigest())
print(len(key.hexdigest()))

hashkey = key.hexdigest()
print(type(hashkey))
print(len(hashkey))