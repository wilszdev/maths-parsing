from parser import parse

if __name__ == '__main__':
    while 1:
        tree = parse(input("calc>>"))
        print(tree.simplify())
