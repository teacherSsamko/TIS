import sys


def main(word):
    print('hello', word)
    print(f'{word}\n'*5)

img_url = sys.argv[-1]
main(img_url)