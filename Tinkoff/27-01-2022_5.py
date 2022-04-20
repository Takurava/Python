def dive(frm, deep, min_deep):
    if frm == need_to_find:
        if min_deep > deep:
            return deep
        return min_deep

    if deep >= min_deep:
        return min_deep

    for i in c[frm]:
        if way[i] == 0:
            way[i] = 1
            min_deep = dive(i, deep + 1, min_deep)
            way[i] = 0

    return min_deep


if __name__ == "__main__":

    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    c = [[] for i in range(n)]
    c_0 = []

    for i in range(n):
        for j in range(0, a[i]+1):
            if i-j+b[i-j] < 0:
                c_0.append(i)
            else:
                if i-j+b[i-j] != i:
                    c[i-j+b[i-j]].append(i)

    if len(c_0) == 0:
        print(-1)
    else:

        c = [list(set(c_el)) for c_el in c]
        c_0 = list(set(c_0))

        for_del = []
        i_del = 0

        for i in range(n):
            if len(c[i]) == 0:
                for_del.append(i)

        while i_del < len(for_del):

            el = for_del[i_del]

            for j in range(n):
                try:
                    c[j].remove(el)
                    if len(c[j]) == 0:
                        for_del.append(j)
                except ValueError:
                    pass

            try:
                c_0.remove(el)
            except ValueError:
                pass

            i_del = i_del+1

        if len(c_0) == 0:
            print(-1)
        else:

            deep_min = n
            need_to_find = n-1
            way = [0 for i in range(n)]

            for i in c_0:
                way[i] = 1
                deep_min = dive(i, 1, deep_min)
                way[i] = 0

            print(deep_min)
