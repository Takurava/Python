if __name__ == "__main__":

    a, b, n = map(int, input().split())

    if a < b:
        print("NO")
    elif a == b and n == 0:
        print("YES")
    else:
        if (a-b) % 2 == 0 and (a-b)//2 >= n:
            print("YES")
        else:
            print("NO")
