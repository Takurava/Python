class Request:

    @staticmethod
    def normal(values, table):
        is_str = []
        if table == 'address':
            is_str = Address.is_str
        elif table == 'candidate':
            is_str = Candidate.is_str
        elif table == 'complaint':
            is_str = Complaint.is_str
        elif table == 'dic_education_level':
            is_str = DicEducationLevel.is_str
        elif table == 'dic_election_commission':
            is_str = DicElectionCommission.is_str
        elif table == 'dic_party':
            is_str = DicParty.is_str
        elif table == 'education':
            is_str = Education.is_str
        elif table == 'election_commission':
            is_str = ElectionCommission.is_str
        elif table == 'observation':
            is_str = Observation.is_str
        elif table == 'participant':
            is_str = Participant.is_str
        elif table == 'person':
            is_str = Person.is_str
        elif table == 'results':
            is_str = Results.is_str

        for i in range(len(is_str)):
            values[i] = str(values[i])
            if is_str[i] == 1 and values[i] != 'null':
                values[i] = ("'" + values[i] + "'")

        return values

    @staticmethod
    def refilling(connection, values, table):
        pattern = []
        rk_count = 0
        if table == 'address':
            pattern = Address.pattern
            rk_count = 1
        elif table == 'candidate':
            pattern = Candidate.pattern
            rk_count = 1
        elif table == 'complaint':
            pattern = Complaint.pattern
            rk_count = 1
        elif table == 'dic_education_level':
            pattern = DicEducationLevel.pattern
            rk_count = 1
        elif table == 'dic_election_commission':
            pattern = DicElectionCommission.pattern
            rk_count = 1
        elif table == 'dic_party':
            pattern = DicParty.pattern
            rk_count = 1
        elif table == 'education':
            pattern = Education.pattern
            rk_count = 1
        elif table == 'election_commission':
            pattern = ElectionCommission.pattern
            rk_count = 1
        elif table == 'observation':
            pattern = Observation.pattern
            rk_count = 1
        elif table == 'participant':
            pattern = Participant.pattern
            rk_count = 2
        elif table == 'person':
            pattern = Person.pattern
            rk_count = 1
        elif table == 'results':
            pattern = Results.pattern
            rk_count = 2

        terms = {pattern[i]: values[i] for i in range(rk_count)}
        print(terms)
        old_row = Request.select(connection, table, terms)
        print(old_row)
        for i in range(len(values)):
            if len(old_row) > 0 and values[i] is None and (pattern[i] not in ['city', 'street', 'house'] or table == 'address'):
                values[i] = old_row[0][i]
            elif values[i] is None:
                values[i] = 'null'
        print(values)
        return values

    @staticmethod
    def select(connection, table, terms):

        with connection.cursor() as cursor:
            expr = 'where ' + ' and '.join([str(el) + ' = ' + str(terms[el]) for el in terms]) if len(terms) > 0 else ''
            query = f'''
                select * 
                from {table}
                {expr} and valid_to_dttm = '9999-12-31 23:59:59'
                '''
            print(query)
            cursor.execute(query)
            print(query)

            result = cursor.fetchall()

        return result

    @staticmethod
    def insert(connection, table, values, with_null=True):
        #Request.normal(values, table)
        print(values)
        with connection.cursor() as cursor:
            query = f"call {table}_insert(null, {', '.join(values)})" if with_null \
                else f"call {table}_insert({', '.join(values)})"
            cursor.execute(query)
            connection.commit()

    @staticmethod
    def update(connection, table, values):
        print(values)
        values = Request.refilling(connection, values, table)
        Request.normal(values, table)
        print(values)
        print(values)
        with connection.cursor() as cursor:
            query = f"call {table}_update({', '.join(values)})"
            cursor.execute(query)
            connection.commit()

    @staticmethod
    def delete(connection, table, values):
        print(values)
        with connection.cursor() as cursor:
            query = f"call {table}_delete({', '.join(values)})"
            cursor.execute(query)
            connection.commit()


class Address:

    pattern = ['address_id', 'city', 'street', 'house']
    is_str = [0, 1, 1, 1]

    @staticmethod
    def get_json(address_id, city, street, house):
        return {'ID': address_id,
                'Город': city,
                'Улица': street,
                'Дом': house}

    @staticmethod
    def select(connection, *terms):
        return Request.select(connection, 'address', *terms)

    @staticmethod
    def select_json(connection, *terms):
        result = Request.select(connection, 'address', *terms)
        return [Address.get_json(row[0], row[1], row[2], row[3]) for row in result]

    @staticmethod
    def insert(connection, *values):
        Request.insert(connection, 'address', *values)

    @staticmethod
    def update(connection, *values):
        Request.update(connection, 'address', *values)

    @staticmethod
    def delete(connection, *terms):
        Request.delete(connection, 'address', *terms)


class Candidate:

    pattern = ['candidate_rk', 'last_name', 'first_name', 'patronymic', 'party_cd']
    is_str = [0, 1, 1, 1, 1]

    @staticmethod
    def get_json(candidate_rk, last_name, first_name, patronymic, party_cd):
        return {'ID': candidate_rk,
                'Фамилия': last_name,
                'Имя': first_name,
                'Отчество': patronymic,
                'Код партии': party_cd}

    @staticmethod
    def select(connection, *terms):
        return Request.select(connection, 'candidate', *terms)

    @staticmethod
    def select_json(connection, *terms):
        result = Request.select(connection, 'candidate', *terms)
        return [Candidate.get_json(row[0], row[1], row[2], row[3], row[4]) for row in result]

    @staticmethod
    def insert(connection, *values):
        Request.insert(connection, 'candidate', *values, False)

    @staticmethod
    def delete(connection, *terms):
        Request.delete(connection, 'candidate', *terms)


class Complaint:

    pattern = ['complaint_id', 'observer_rk', 'message', 'treatment_flg', 'success_flg']
    is_str = [0, 0, 1, 0, 0]

    @staticmethod
    def get_json(complaint_id, observer_rk, message, treatment_flg, success_flg):
        return {'ID': complaint_id,
                'ID наблюдателя': observer_rk,
                'Сообщение': message,
                'Флаг обработки': treatment_flg,
                'Флаг решения': success_flg}

    @staticmethod
    def select(connection, *terms):
        return Request.select(connection, 'complaint', *terms)

    @staticmethod
    def select_json(connection, *terms):
        result = Request.select(connection, 'complaint', *terms)
        return [Complaint.get_json(row[0], row[1], row[2], row[3], row[4]) for row in result]

    @staticmethod
    def insert(connection, *values):
        Request.insert(connection, 'complaint', *values, False)

    @staticmethod
    def update(connection, *values):
        Request.update(connection, 'complaint', *values)

    @staticmethod
    def delete(connection, *terms):
        Request.delete(connection, 'complaint', *terms)


class DicEducationLevel:

    pattern = ['education_level_cd', 'education_level_desc']
    is_str = [1, 1]

    @staticmethod
    def get_json(education_level_cd, education_level_desc):
        return {'Код': education_level_cd,
                'Описание': education_level_desc}

    @staticmethod
    def select(connection, *terms):
        return Request.select(connection, 'dic_education_level', *terms)

    @staticmethod
    def select_json(connection, *terms):
        result = Request.select(connection, 'dic_education_level', *terms)
        return [DicEducationLevel.get_json(row[0], row[1]) for row in result]

    @staticmethod
    def insert(connection, *values):
        Request.insert(connection, 'dic_education_level', *values, False)

    @staticmethod
    def delete(connection, *terms):
        Request.delete(connection, 'dic_education_level', *terms)


class DicElectionCommission:

    pattern = ['election_commission_cd', 'election_commission_desc']
    is_str = [1, 1]

    @staticmethod
    def get_json(election_commission_cd, election_commission_desc):
        return {'Код': election_commission_cd,
                'Описание': election_commission_desc}

    @staticmethod
    def select(connection, *terms):
        return Request.select(connection, 'dic_election_commission', *terms)

    @staticmethod
    def select_json(connection, *terms):
        result = Request.select(connection, 'dic_election_commission', *terms)
        return [DicElectionCommission.get_json(row[0], row[1]) for row in result]

    @staticmethod
    def insert(connection, *values):
        Request.insert(connection, 'dic_election_commission', *values, False)

    @staticmethod
    def delete(connection, *terms):
        Request.delete(connection, 'dic_election_commission', *terms)


class DicParty:

    pattern = ['party_cd', 'party_desc']
    is_str = [1, 1]

    @staticmethod
    def get_json(party_cd, party_desc):
        return {'Код': party_cd,
                'Описание': party_desc}

    @staticmethod
    def select(connection, *terms):
        return Request.select(connection, 'dic_party', *terms)

    @staticmethod
    def select_json(connection, *terms):
        result = Request.select(connection, 'dic_party', *terms)
        return [DicParty.get_json(row[0], row[1]) for row in result]

    @staticmethod
    def insert(connection, *values):
        Request.insert(connection, 'dic_party', *values, False)

    @staticmethod
    def delete(connection, *terms):
        Request.delete(connection, 'dic_party', *terms)


class Education:

    pattern = ['education_id', 'organizer_rk', 'open_dttm', 'duration_tm',
               'education_level_cd', 'participants_limit', 'city', 'street', 'house']
    is_str = [0, 0, 1, 1, 1, 1, 1, 0, 0]

    @staticmethod
    def get_json(education_id, organizer_rk, open_dttm, duration_tm, address_id, education_level_cd,
                 participants_limit):
        return {'ID': education_id,
                'ID организатора': organizer_rk,
                'Дата начала': open_dttm,
                'Длительность': duration_tm,
                'ID адреса': address_id,
                'Код уровня обучения': education_level_cd,
                'Лимит участников': participants_limit}

    @staticmethod
    def select(connection, *terms):
        return Request.select(connection, 'education', *terms)

    @staticmethod
    def select_json(connection, *terms):
        result = Request.select(connection, 'education', *terms)
        return [Education.get_json(row[0], row[1], row[2], row[3], row[4], row[5], row[6]) for row in result]

    @staticmethod
    def insert(connection, *values):
        Request.insert(connection, 'education', *values, False)

    @staticmethod
    def update(connection, *values):
        Request.update(connection, 'education', *values)

    @staticmethod
    def delete(connection, *terms):
        Request.delete(connection, 'education', *terms)


class ElectionCommission:

    pattern = ['election_commission_rk', 'num', 'election_commission_cd', 'city', 'street', 'house']
    is_str = [0, 0, 1, 1, 1, 1]

    @staticmethod
    def get_json(election_commission_rk, num, election_commission_cd, address_id):
        return {'ID': election_commission_rk,
                'Номер': num,
                'Код уровня ИК': election_commission_cd,
                'ID адреса': address_id}

    @staticmethod
    def select(connection, *terms):
        return Request.select(connection, 'election_commission', *terms)

    @staticmethod
    def select_json(connection, *terms):
        result = Request.select(connection, 'election_commission', *terms)
        return [ElectionCommission.get_json(row[0], row[1], row[2], row[3]) for row in result]

    @staticmethod
    def insert(connection, *values):
        Request.insert(connection, 'election_commission', *values, False)

    @staticmethod
    def update(connection, *values):
        Request.update(connection, 'election_commission', *values)

    @staticmethod
    def delete(connection, *terms):
        Request.delete(connection, 'election_commission', *terms)


class Observation:

    pattern = ['observation_id', 'observer_rk', 'election_commission_rk', 'observation_dt']
    is_str = [0, 0, 0, 1]

    @staticmethod
    def get_json(observation_id, observer_rk, election_commission_rk, observation_dt):
        return {'ID': observation_id,
                'ID наблюдателя': observer_rk,
                'ID ИК': election_commission_rk,
                'Дата наблюдения': observation_dt}

    @staticmethod
    def select(connection, *terms):
        return Request.select(connection, 'observation', *terms)

    @staticmethod
    def select_json(connection, *terms):
        result = Request.select(connection, 'observation', *terms)
        return [Observation.get_json(row[0], row[1], row[2], row[3]) for row in result]

    @staticmethod
    def insert(connection, *values):
        Request.insert(connection, 'observation', *values, False)

    @staticmethod
    def delete(connection, *terms):
        Request.delete(connection, 'observation', *terms)


class Participant:

    pattern = ['observer_rk', 'education_id']
    is_str = [0, 0]

    @staticmethod
    def get_json(observer_rk, education_id):
        return {'ID наблюдателя': observer_rk,
                'ID ИК': education_id}

    @staticmethod
    def select(connection, *terms):
        return Request.select(connection, 'participant', *terms)

    @staticmethod
    def select_json(connection, *terms):
        result = Request.select(connection, 'participant', *terms)
        return [Participant.get_json(row[0], row[1]) for row in result]

    @staticmethod
    def insert(connection, *values):
        Request.insert(connection, 'participant', *values, False)

    @staticmethod
    def delete(connection, *terms):
        Request.delete(connection, 'participant', *terms)


class Person:

    pattern = ('person_rk', 'last_name', 'first_name', 'patronymic', 'phone_number', 'admin_flg', 'observer_flg',
               'organizer_flg', 'login', 'hash_password', 'city', 'street', 'house')
    is_str = [0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1]

    @staticmethod
    def get_json(person_rk, last_name, first_name, patronymic, phone_number, admin_flg, observer_flg, organizer_flg,
                 login, hash_password, address_id):
        return {'ID': person_rk,
                'Фамилия': last_name,
                'Имя': first_name,
                'Отчество': patronymic,
                'Телефон': phone_number,
                'Флаг администратора': admin_flg,
                'Флаг наблюдателя': observer_flg,
                'Флаг организатора': organizer_flg,
                'Логин': login,
                'Пароль': hash_password,
                'ID адреса': address_id}

    @staticmethod
    def select(connection, *terms):
        return Request.select(connection, 'person', *terms)

    @staticmethod
    def select_json(connection, *terms):
        result = Request.select(connection, 'person', *terms)
        return [Person.get_json(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],
                                row[10]) for row in result]

    @staticmethod
    def insert(connection, *values):
        Request.insert(connection, 'person', *values, False)

    @staticmethod
    def update(connection, *values):
        Request.update(connection, 'person', *values)

    @staticmethod
    def delete(connection, *terms):
        Request.delete(connection, 'person', *terms)


class Results:

    pattern = ['candidate_rk', 'election_commission_rk', 'count', 'success_flg']
    is_str = [0, 0, 0, 0]

    @staticmethod
    def get_json(candidate_rk, election_commission_rk, count, success_flg):
        return {'ID': candidate_rk,
                'Фамилия': election_commission_rk,
                'Имя': count,
                'Отчество': success_flg}

    @staticmethod
    def select(connection, *terms):
        return Request.select(connection, 'results', *terms)

    @staticmethod
    def select_json(connection, *terms):
        result = Request.select(connection, 'results', *terms)
        return [Results.get_json(row[0], row[1], row[2], row[3]) for row in result]

    @staticmethod
    def insert(connection, *values):
        Request.insert(connection, 'results', *values, False)

    @staticmethod
    def update(connection, *values):
        Request.update(connection, 'results', *values)

    @staticmethod
    def delete(connection, *terms):
        Request.delete(connection, 'results', *terms)
