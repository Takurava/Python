import math


def min_max(a1, b1):
    if a1 > b1:
        return b1, a1
    else:
        return a1, b1


if __name__ == "__main__":

    n, m = map(int, input().split())

    if (n+m - 2) % 3 != 0:
        print(0)
    else:
        x, y = min_max(n, m)

        if y - 2*x > 0:
            print(0)
        else:

            a = (2*x - y - 1) // 3
            b = (2*y - x - 1) // 3

            fact = 1

            n = a+b
            k = a

            for i in range(a+b, b, -1):
                fact = fact * i
            for i in range(1, a+1, 1):
                fact = fact // i

            print(fact)
