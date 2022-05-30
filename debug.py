PRINT_DEBUG = False


def print(*args):
    if PRINT_DEBUG:
        for arg in args:
            print(arg, end=' ')
        print()
