
def charge_insert(connection, flat, amount):

    insert_query = f'''insert into charges (id_flat, amount, charge_date) 
                        value((select id from flat where num = {str(flat)}), {str(amount)}, now())'''

    with connection.cursor() as cursor:
        cursor.execute(insert_query)
        connection.commit()

    print('Success.')


def payment_insert(connection, flat, year, month, day, amount):

    insert_query = f'''insert into payments (id_flat, amount, payment_date) 
                            value((select id from flat where num = {str(flat)}), {str(amount)}, 
                            '{year}-{month}-{day}')'''

    with connection.cursor() as cursor:
        cursor.execute(insert_query)
        connection.commit()

    print('Success.')


def flat_insert(connection, number):

    print(number)

    insert_query = f'insert into flat (num) value ({str(number)})'

    with connection.cursor() as cursor:
        cursor.execute(insert_query)
        connection.commit()
        print(cursor)
