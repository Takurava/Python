def add_info(cities, name, direction, index):
    try:
        city = cities[name]
    except KeyError:
        city = {'in' : [], 'out' : []}
        cities.update({name : city})
    city[direction].append(index)


def fill_cities (str_arr):
    cities = {}
    len_str_arr = len(str_arr)
    for card_ind in range(len_str_arr): 
        card = str_arr[card_ind]
        add_info(cities, card[0], 'out', card_ind)
        add_info(cities, card[1],  'in', card_ind)
    return cities


def find_start(cities):
    for city in cities:
        in_count = len(cities[city]['in'])
        out_count = len(cities[city]['out'])
        if out_count > in_count:
            return city
     

def given_arr(arr):  
    return '\n' + '\n'.join([f'{i[0]} -> {i[1]}' for i in arr])


def result_arr(arr, res):
    return f'{arr[res[0]][0]} -> ' + ' -> '.join([arr[i][1] for i in res])


def find_path(str_arr):
    print(given_arr(str_arr))
    cities = fill_cities(str_arr)
    start = find_start(cities)
    result = []
    while True:
        ind = cities[start]['out'][0]
        end = str_arr[ind][1]

        result.append(ind)
        cities[start]['out'].remove(ind)
        cities[end]['in'].remove(ind)
        start = end
        if (len(cities[start]['out']) == 0):
            break
    
    print(result_arr(str_arr, result))

    return result