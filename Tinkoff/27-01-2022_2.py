def min_max(a, b):
    if a > b:
        return b, a
    else:
        return a, b


if __name__ == "__main__":

    n, m = map(int, input().split())
    count = 0

    while m > 0:
        n, m = min_max(n, m)
        count = count + (m // n)
        m = m % n

    print(count)
