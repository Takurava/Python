import math


if __name__ == "__main__":

    n = int(input())
    a = list(map(int, input().split()))
    a.sort(reverse=True)

    x = 0

    for a_i in a:
        x = math.ceil((a_i + x)**0.5)

    print(x)
