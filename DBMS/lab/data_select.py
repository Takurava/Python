
def flat_select(connection):

    insert_query = 'select num from flat'

    result = []

    with connection.cursor() as cursor:
        cursor.execute(insert_query)
        query = cursor.fetchall()
        for row in query:

            result.append(row[0])

    print('Success.')
    return result
