import sys


if __name__ == "__main__":
    arguments = sys.argv

    for argument in arguments:
        print(argument)
    print('Number of arguments:', len(sys.argv), 'arguments.')
    print('Argument List:', str(sys.argv))
