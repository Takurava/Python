import copy
from decimal import Decimal


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def turnover_statement(connection, year):

    select_query = f'''select f.num, f.m, coalesce(charg.s, 0) charge_sum, 
                            coalesce(pay.s, 0) payment_sum, coalesce(sald.s, 0) saldo_sum
                        from (select id, num, m
		                    from (select id, num from flat) f,
			                        (select 1 m union select 2 union select 3 union select 4 
			                        union select 5 union select 6 union select 7 union select 8 
			                        union select 9 union select 10 union select 11 union select 12) m) f
                        left join (select id_flat, month(charge_date) m, sum(amount) s
                                    from charges 
                                    where charge_date between '{year}-01-01' and '{year}-12-31'
                                    group by 1, 2) charg on f.id = charg.id_flat and f.m = charg.m
                        left join (select id_flat, month(payment_date) m, sum(amount) s
                                    from payments 
                                    where payment_date between '{year}-01-01' and '{year}-12-31'
                                    group by 1, 2) pay on f.id = pay.id_flat and f.m = pay.m
                        left join (select id_flat, month(saldo_date) m, sum(amount) s
                                    from saldo 
                                    where saldo_date between '{year}-01-02' and '{year + 1}-01-01'
                                    group by 1, 2) sald on f.id = sald.id_flat and f.m = sald.m'''

    cell_model = {'charge': 0.0,
                  'payment': 0.0,
                  'saldo': 0.0}
    row_model = {'flat': -1,
                 'input-saldo': 0.0,
                 'monthly-information': {x: copy.deepcopy(cell_model) for x in range(1, 13)},
                 'output-saldo': 0.0}

    result = []

    with connection.cursor() as cursor:
        cursor.execute(select_query)
        query = cursor.fetchall()
        for row in query:
            print(row)

            flat = None

            for flat_row in result:
                if row[0] == flat_row['flat']:
                    flat = flat_row
            if flat is None:
                flat = copy.deepcopy(row_model)
                flat['flat'] = row[0]
                result.append(flat)

            flat['monthly-information'][row[1]]['charge'] = float(row[2])
            flat['monthly-information'][row[1]]['payment'] = float(row[3])
            flat['monthly-information'][row[1]]['saldo'] = float(row[4])

        for flat in result:
            flat['input-saldo'] = flat['monthly-information'][1]['saldo'] - \
                                  flat['monthly-information'][1]['charge'] + \
                                  flat['monthly-information'][1]['payment']
            flat['output-saldo'] = flat['monthly-information'][12]['saldo']

    return result


def charges_and_payments_by_month(connection, year, flat):

    select_query = f'''select m.m, coalesce(charg.s, 0) charge_sum, coalesce(pay.s, 0) payment_sum, 
                            coalesce(sald.s, 0) saldo_sum
                        from (select 1 m union select 2 union select 3 union select 4 
                                union select 5 union select 6 union select 7 union select 8 
                                union select 9 union select 10 union select 11 union select 12) m
                        left join (select month(charge_date) m, sum(amount) s
                                    from charges 
                                    where id_flat in (select id from flat where num = {flat}) and charge_date between '{year}-01-01' and '{year}-12-31'
                                    group by 1) charg on m.m = charg.m
                        left join (select month(payment_date) m, sum(amount) s
                                    from payments 
                                    where id_flat in (select id from flat where num = {flat}) and payment_date between '{year}-01-01' and '{year}-12-31'
                                    group by 1) pay on m.m = pay.m
                        left join (select month(saldo_date) m, sum(amount) s
                                    from saldo 
                                    where id_flat in (select id from flat where num = {flat}) and saldo_date between '{year}-01-02' and '{year + 1}-01-01'
                                    group by 1) sald on m.m = sald.m'''

    column_model = {'charge': 0.0,
                    'payment': 0.0}
    row_model = {'input-saldo': 0.0,
                 'monthly-information': {x: copy.deepcopy(column_model) for x in range(1, 13)},
                 'total': copy.deepcopy(column_model),
                 'delta-saldo': 0.0,
                 'output-saldo': 0.0}

    result = copy.deepcopy(row_model)

    with connection.cursor() as cursor:
        cursor.execute(select_query)
        query = cursor.fetchall()

        saldo = []

        for row in query:
            print(row)
            result['monthly-information'][row[0]]['charge'] = float(row[1])
            result['monthly-information'][row[0]]['payment'] = float(row[2])
            saldo.append(float(row[3]))

        for month in reversed(result['monthly-information']):
            if result['monthly-information'][month]['charge'] == 0 and \
                    result['monthly-information'][month]['payment'] == 0:
                continue
            else:
                result['output saldo'] = saldo[month - 1]
                break

        result['input-saldo'] = saldo[0] - result['monthly-information'][1]['charge'] + \
                                result['monthly-information'][1]['payment']

        result['total']['charge'] = sum(value['charge'] for value in result['monthly-information'].values())
        result['total']['payment'] = sum(value['payment'] for value in result['monthly-information'].values())

        result['delta-saldo'] = result['total']['charge'] - \
                                result['total']['payment']

    return result


def debtors_by_category(connection, year, month, day):

    select_query = f'''select flat.num, coalesce(charg.s, 0) charge_sum, coalesce(sald.s, 0) saldo_sum, 
                            debtor_category('{year}-{month}-01' + interval 1 month, flat.id)
                        from flat
                        left join (select id_flat, sum(amount) s
                                    from charges
                                    where charge_date between '{year}-{month}-01' and 
                                        ('{year}-{month}-01' + interval 1 month - interval 1 day)
                                    group by 1) charg on flat.id = charg.id_flat
                        left join (select id_flat, sum(amount) s
                                    from saldo
                                    where saldo_date between '{year}-{month}-02' and 
                                        ('{year}-{month}-01' + interval 1 month)
                                    group by 1) sald on flat.id = sald.id_flat
                        where debtor_category(('{year}-{month}-01' + interval 1 month), flat.id) > 0'''

    row_model = {'flat': -1,
                 'last-month-charge': 0,
                 'saldo': 0,
                 'arrears': {x: '' for x in range(1, 5)}}

    result = []

    with connection.cursor() as cursor:
        cursor.execute(select_query)
        query = cursor.fetchall()
        for row in query:
            print(row)

            flat = None

            flat = copy.deepcopy(row_model)
            flat['flat'] = row[0]
            result.append(flat)

            flat['last-month-charge'] = float(row[1])
            flat['saldo'] = float(row[2])

            flat['arrears'][row[3]] = float(row[2])

    return result
