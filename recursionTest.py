def main():
    x = 5
    print(recurseThing(x))

def recurseThing(y):
    if (y > 0):
        print(y)
        return recurseThing(y-1)
    else:
        print(y)
        return 0

main()