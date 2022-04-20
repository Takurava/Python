def total_results(connection):
    query = f'''
        select CONCAT(last_name, ' ', first_name, ' ', patronymic) as person,
        num,
        count
        from results r
        left join candidate c
                on r.candidate_rk = c.candidate_rk
                and c.valid_to_dttm = '9999-12-31 23:59:59'
        left join election_commission ec
                on r.election_commission_rk = ec.election_commission_rk
                and ec.valid_to_dttm = '9999-12-31 23:59:59'
        where r.success_flg = TRUE
        order by 2, 3
                
    '''

    result = []

    with connection.cursor() as cursor:
        cursor.execute(query)
        query = cursor.fetchall()
        for row in query:
            result.append({'candidate': row[0],
                           'election_commission': row[1],
                           'result': row[2]})
            
    return result


def results_by_candidate(connection, candidate_rk):
    query = f'''
        select num,
        count
        from candidate c
            left join results r
                on r.candidate_rk = c.candidate_rk
                and r.success_flg = TRUE
        left join election_commission ec
                on r.election_commission_rk = ec.election_commission_rk
                and ec.valid_to_dttm = '9999-12-31 23:59:59'
        where c.valid_to_dttm = '9999-12-31 23:59:59'
            and c.candidate_rk = {candidate_rk}
        order by 1, 2
    '''

    result = []

    with connection.cursor() as cursor:
        cursor.execute(query)
        query = cursor.fetchall()
        for row in query:
            result.append({'election_commission': row[0],
                           'result': row[1]})
            
    return result


def observer_profile(connection, person_rk):
    query = f'''
        select last_name, 
            first_name,
            patronymic,
            phone_number, 
            CONCAT(a1.city, ' ', a1.street, ' ', a1.house) as address1,
            num, 
            CONCAT(a2.city, ' ', a2.street, ' ', a2.house) as address1
        from person p
            left join observation o
                    on p.person_rk = o.observer_rk
                    and o.valid_to_dttm = '9999-12-31 23:59:59'
                left join election_commission ec
                        on o.election_commission_rk = ec.election_commission_rk
                        and ec.valid_to_dttm = '9999-12-31 23:59:59'
                    left join address a2
                            on ec.address_id = a2.address_id
                            and a2.valid_to_dttm = '9999-12-31 23:59:59'
            left join address a1
                    on p.address_id = a1.address_id
                    and a1.valid_to_dttm = '9999-12-31 23:59:59'
        where p.person_rk = {person_rk} and p.observer_flg = TRUE and p.valid_to_dttm = '9999-12-31 23:59:59'
    '''

    result = []

    with connection.cursor() as cursor:
        cursor.execute(query)
        query = cursor.fetchall()
        for row in query:
            result.append({'last_name': row[0],
                           'first name': row[1],
                           'patronymic': row[2],
                           'phone number': row[3],
                           'address': row[4],
                           'election commission': row[5],
                           'election commission address': row[6]})
    return result


def organizer_profile(connection, person_rk):
    query = f'''
        select last_name, 
            first_name,
            patronymic,
            phone_number, 
            CONCAT(a1.city, ' ', a1.street, ' ', a1.house) as address1,
        from person p
            left join address a1
                    on p.address_id = a1.address_id
                    and a1.valid_to_dttm = '9999-12-31 23:59:59'
        where p.person_rk = {person_rk} and p.observer_flg = TRUE and p.valid_to_dttm = '9999-12-31 23:59:59'
    '''

    result = []

    with connection.cursor() as cursor:
        cursor.execute(query)
        query = cursor.fetchall()
        for row in query:
            result.append({'last_name': row[0],
                           'first name': row[1],
                           'patronymic': row[2],
                           'phone number': row[3],
                           'address': row[4]})

    return result


def organizer_training(connection, person_rk):
    query = f'''
        select education_level_desc,
            open_dttm,
            duration_tm,
            participants_limit,
            CONCAT(a1.city, ' ', a1.street, ' ', a1.house) as address1
        from education e
            left join address a1
                    on e.address_id = a1.address_id
                    and a1.valid_to_dttm = '9999-12-31 23:59:59'
            left join dic_education_level de
                    on e.education_level_cd = de.education_level_cd
                    and de.valid_to_dttm = '9999-12-31 23:59:59'
        where 
            organizer_rk = {person_rk} and e.valid_to_dttm = '9999-12-31 23:59:59' and open_dttm > now()
    '''

    result = []

    with connection.cursor() as cursor:
        cursor.execute(query)
        query = cursor.fetchall()
        for row in query:
            result.append({'education level': row[0],
                           'open dttm': row[1],
                           'duration tm': row[2],
                           'participants limit': row[3],
                           'address': row[4]})
    return result


def observer_training(connection, person_rk):
    query = f'''
    select education_level_desc,
            open_dttm,
            duration_tm,
            CONCAT(a1.city, ' ', a1.street, ' ', a1.house) as address1
        from education e
            left join address a1
                    on e.address_id = a1.address_id
                    and a1.valid_to_dttm = '9999-12-31 23:59:59'
            left join dic_education_level de
                    on e.education_level_cd = de.education_level_cd
                    and de.valid_to_dttm = '9999-12-31 23:59:59'
        where 
            e.valid_to_dttm = '9999-12-31 23:59:59' and open_dttm > now() 
            and participants_limit > (
                select count(*) 
                from participant p 
                where p.education_id = e.education_id and p.valid_to_dttm = '9999-12-31 23:59:59'
            )
            and {person_rk} not in (select observer_rk 
                from participant p 
                where p.education_id = e.education_id and p.valid_to_dttm = '9999-12-31 23:59:59')
    '''

    result = []

    with connection.cursor() as cursor:
        cursor.execute(query)
        query = cursor.fetchall()
        for row in query:
            result.append({'education level': row[0],
                           'open dttm': row[1],
                           'duration tm': row[2],
                           'address': row[3]})
    return result


def participant_training(connection, person_rk):
    query = f'''
        'select education_level_desc,
            open_dttm,
            duration_tm,
            CONCAT(a1.city, ' ', a1.street, ' ', a1.house) as address1
        from participant p
            left join education e
                    on p.education_id = e.education_id
                    and e.valid_to_dttm = '9999-12-31 23:59:59'
                left join address a1
                        on e.address_id = a1.address_id
                        and a1.valid_to_dttm = '9999-12-31 23:59:59'
                left join dic_education_level de
                        on e.education_level_cd = de.education_level_cd
                        and de.valid_to_dttm = '9999-12-31 23:59:59'
        where 
            {person_rk} = observer_rk and open_dttm > now() and p.valid_to_dttm = '9999-12-31 23:59:59'
    '''

    result = []

    with connection.cursor() as cursor:
        cursor.execute(query)
        query = cursor.fetchall()
        for row in query:
            result.append({'education level': row[0],
                           'open dttm': row[1],
                           'duration tm': row[2],
                           'address': row[3]})
    return result


def total_observation(connection):
    query = f'''
        select num, 
            CONCAT(a1.city, ' ', a1.street, ' ', a1.house) as address1,
             CONCAT(last_name, ' ', first_name) as person
        from observation o
            left join person p
                    on p.person_rk= o.observer_rk
                    and p.valid_to_dttm = '9999-12-31 23:59:59'
            left join election_commission ec
                    on ec.election_commission_rk= o.election_commission_rk
                    and ec.valid_to_dttm = '9999-12-31 23:59:59'
                left join address a1
                    on a1.address_id= ec.address_id
                    and a1.valid_to_dttm = '9999-12-31 23:59:59'
        where o.valid_to_dttm = '9999-12-31 23:59:59'
                
    '''

    result = []

    with connection.cursor() as cursor:
        cursor.execute(query)
        query = cursor.fetchall()
        for row in query:
            result.append({'election commission': row[0],
                           'election commission address': row[1],
                           'observer': row[2]})

    return result


def lost_election_commission(connection):
    query = f'''
        select num, 
            CONCAT(a1.city, ' ', a1.street, ' ', a1.house) as address1
        from election_commission es
            left join observation o
                    on es.election_commission_rk= o.election_commission_rk
                    and o.valid_to_dttm = '9999-12-31 23:59:59'
                left join person p
                    on p.person_rk= o.observer_rk
                    and p.valid_to_dttm = '9999-12-31 23:59:59'
            left join address a1
                on a1.address_id= es.address_id
                and a1.valid_to_dttm = '9999-12-31 23:59:59'
        where es.valid_to_dttm = '9999-12-31 23:59:59' and person_rk is null
    '''

    result = []

    with connection.cursor() as cursor:
        cursor.execute(query)
        query = cursor.fetchall()
        for row in query:
            result.append({'election commission': row[0],
                           'election commission address': row[1]})
    return result


def lost_observer(connection):
    query = f'''
        select CONCAT(last_name, ' ', first_name) as person, 
            CONCAT(a1.city, ' ', a1.street, ' ', a1.house) as address1
        from person p
            left join observation o
                    on p.person_rk= o.observer_rk
                    and o.valid_to_dttm = '9999-12-31 23:59:59'
                left join election_commission ec
                    on ec.election_commission_rk= o.election_commission_rk
                    and p.valid_to_dttm = '9999-12-31 23:59:59'
            left join address a1
                on a1.address_id= p.address_id
                and a1.valid_to_dttm = '9999-12-31 23:59:59'
        where p.valid_to_dttm = '9999-12-31 23:59:59' and ec.election_commission_rk is null
    '''

    result = []

    with connection.cursor() as cursor:
        cursor.execute(query)
        query = cursor.fetchall()
        for row in query:
            result.append({'observer': row[0],
                           'observer address': row[1]})
    return result


def candidates_list(connection):
    query = f'''
        select last_name, 
             first_name, 
             patronymic, 
             party_desc
        from candidate c
            left join dic_party dp
                    on c.party_cd = dp.party_cd
                    and dp.valid_to_dttm = '9999-12-31 23:59:59'
        where c.valid_to_dttm = '9999-12-31 23:59:59'
    '''

    result = []

    with connection.cursor() as cursor:
        cursor.execute(query)
        query = cursor.fetchall()
        for row in query:
            result.append({'last name': row[0],
                           'first name': row[1],
                           'patronymic': row[2],
                           'party': row[3]})
    return result


def dic_education_level(connection):
    query = f'''
        select education_level_cd, education_level_desc
        from dic_education_level
        where valid_to_dttm = '9999-12-31 23:59:59'
    '''

    result = []

    with connection.cursor() as cursor:
        cursor.execute(query)
        query = cursor.fetchall()
        for row in query:
            result.append({'education level': row[0],
                           'description': row[1]})

    return result


def dic_election_commission(connection):
    query = f'''
        select election_commission_cd, election_commission_desc
        from dic_election_commission
        where valid_to_dttm = '9999-12-31 23:59:59'
    '''

    result = []

    with connection.cursor() as cursor:
        cursor.execute(query)
        query = cursor.fetchall()
        for row in query:
            result.append({'election commission': row[0],
                           'description': row[1]})
    return result


def dic_party(connection):
    query = f'''
        select party_cd, party_desc
        from valid_to_dttm
        where valid_to_dttm = '9999-12-31 23:59:59'
    '''

    result = []

    with connection.cursor() as cursor:
        cursor.execute(query)
        query = cursor.fetchall()
        for row in query:
            result.append({'party': row[0],
                           'description': row[1]})
    return result


def total_complaints(connection):
    query = f'''
        select complaint_id, 
            message, 
            treatment_flg,
            success_flg,
            CONCAT(last_name, ' ', first_name) as person,
            num, 
            CONCAT(a1.city, ' ', a1.street, ' ', a1.house) as address1
        from complaint c
            left join person p
                    on p.person_rk= c.observer_rk
                    and p.valid_to_dttm = '9999-12-31 23:59:59'
                left join observation o
                        on p.person_rk= o.observer_rk
                        and o.valid_to_dttm = '9999-12-31 23:59:59'
                    left join election_commission ec
                            on ec.election_commission_rk= o.election_commission_rk
                            and ec.valid_to_dttm = '9999-12-31 23:59:59'
                        left join address a1
                            on a1.address_id= ec.address_id
                            and a1.valid_to_dttm = '9999-12-31 23:59:59'
        where c.valid_to_dttm = '9999-12-31 23:59:59'
            
    '''

    result = []

    with connection.cursor() as cursor:
        cursor.execute(query)
        query = cursor.fetchall()
        for row in query:
            result.append({'complaint id': row[0],
                           'message': row[1],
                           'treatment flg': row[2],
                           'success flg': row[3],
                           'observe': row[4],
                           'election_commission': row[5],
                           'election_commission address': row[6]})
    return result


def observer_complaints(connection, person_rk):
    query = f'''
        select complaint_id, 
            message, 
            treatment_flg,
            success_flg,
        from complaint c
            left join person p
                    on p.person_rk= c.observer_rk
                    and p.valid_to_dttm = '9999-12-31 23:59:59'
        where c.valid_to_dttm = '9999-12-31 23:59:59' and p.person_rk= {person_rk}
    '''

    result = []

    with connection.cursor() as cursor:
        cursor.execute(query)
        query = cursor.fetchall()
        for row in query:
            result.append({'complaint id': row[0],
                           'message': row[1],
                           'treatment flg': row[2],
                           'success flg': row[3]})
    return result


def one_complaint(connection, complaint_id):
    query = f'''
        select complaint_id, 
            message, 
            treatment_flg,
            success_flg,
            CONCAT(last_name, ' ', first_name) as person,
            num, 
            CONCAT(a1.city, ' ', a1.street, ' ', a1.house) as address1
        from complaint c
            left join person p
                    on p.person_rk= c.observer_rk
                    and p.valid_to_dttm = '9999-12-31 23:59:59'
                left join observation o
                        on p.person_rk= o.observer_rk
                        and o.valid_to_dttm = '9999-12-31 23:59:59'
                    left join election_commission ec
                            on ec.election_commission_rk= o.election_commission_rk
                            and ec.valid_to_dttm = '9999-12-31 23:59:59'
                        left join address a1
                            on a1.address_id= ec.address_id
                            and a1.valid_to_dttm = '9999-12-31 23:59:59'
        where c.valid_to_dttm = '9999-12-31 23:59:59' complaint_id = {complaint_id}
    '''

    result = []

    with connection.cursor() as cursor:
        cursor.execute(query)
        query = cursor.fetchall()
        for row in query:
            result.append({'complaint id': row[0],
                           'message': row[1],
                           'treatment flg': row[2],
                           'success flg': row[3],
                           'observe': row[4],
                           'election_commission': row[5],
                           'election_commission address': row[6]})

    return result
