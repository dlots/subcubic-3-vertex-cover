PRINT_DEBUG = False


def debug(*args):
    if PRINT_DEBUG:
        for arg in args:
            print(arg, end=' ')
        print()
