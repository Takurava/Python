from mysql.connector import connect, Error
from flask_cors import CORS
import data_insert
import summaries
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from flask import Flask
from flask import request
import json
import data_select


class Server(object):

    def index(self):
        return 'Hello, World!'

    def turnover_statement(self):
        year  = request.args.get('year', default = 1, type = int)

        return json.dumps(summaries.turnover_statement(self.db, year))

    def charges_and_payments_by_month(self):
        year  = request.args.get('year', default = 1, type = int)
        flat  = request.args.get('flat', default = 1, type = int)

        return json.dumps(summaries.charges_and_payments_by_month(self.db, year, flat))

    def debtors_by_category(self):
        year  = request.args.get('year', default = 1, type = int)
        month = request.args.get('month', default = 1, type = int)
        day   = request.args.get('day', default = 1, type = int)

        return json.dumps(summaries.debtors_by_category(self.db, year, month, day))

    def flat_insert(self):
        data = request.get_json()
        print(data)
        try:
            data_insert.flat_insert(self.db, data['flat_number'])
        except Error as e:
            print(e)
            return str(e), 500

        return 'created', 201

    def charge_insert(self):
        data = request.get_json()
        print(data)
        try:
            data_insert.charge_insert(self.db, data['flat_number'], data['amount'])
        except Error as e:
            print(e)
            return str(e), 500

        return 'created', 201

    def payment_insert(self):
        data = request.get_json()
        print(data)
        try:
            data_insert.payment_insert(self.db, data['flat_number'],
                                    data['year'], data['month'], data['day'],
                                    data['amount'])
        except Error as e:
            print(e)
            return str(e), 500

        return 'created', 201

    def flat_select(self):
        return json.dumps(data_select.flat_select(self.db))

    def __init__(self):
        self.db = connect(
                    host="localhost",
                    user="python_user",
                    password="QWEasd_123",
                    database="lab",
            )

        self.app = Flask(__name__)
        CORS(self.app)

        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/statement', 'statement', self.turnover_statement, methods=['GET'])
        self.app.add_url_rule('/month', 'month', self.charges_and_payments_by_month, methods=['GET'])
        self.app.add_url_rule('/debtors', 'debtors', self.debtors_by_category, methods=['GET'])
        self.app.add_url_rule('/flat', 'flat', self.flat_insert, methods=['POST'])
        self.app.add_url_rule('/charge', 'charge', self.charge_insert, methods=['POST'])
        self.app.add_url_rule('/payment', 'payment', self.payment_insert, methods=['POST'])
        self.app.add_url_rule('/flat/all', 'all_flat', self.flat_select, methods=['GET'])

    def __del__(self):
        self.db.close()

'''
        @app.route('/debtors', methods=['GET'])
        def debtors_by_category():

            return 'Hello, World!' '''



'''
    summaries.turnover_statement(connection)
    summaries.charges_and_payments_by_month(connection)
    summaries.debtors_by_category(connection)
    data_insert.flat_insert(connection)
    data_insert.charge_insert(connection)
    data_insert.payment_insert(connection)
'''


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('PyCharm')

    srv = Server()

    srv.app.run()

'''
    while True:
        try:
            with connect(
                    host="localhost",
                    user="python_user",
                    password="QWEasd_123",
                    database="lab",
            ) as connection:

                while True:
                    print('1. Turnover statement')
                    print('2. Charges and payments by month')
                    print('3. Debtors by category')
                    print('4. Insert into flat')
                    print('5. Insert into charges')
                    print('6. Insert into payments')
                    table_number = input()
                    if table_number == '1':
                        summaries.turnover_statement(connection)
                    elif table_number == '2':
                        summaries.charges_and_payments_by_month(connection)
                    elif table_number == '3':
                        summaries.debtors_by_category(connection)
                    elif table_number == '4':
                        data_insert.flat_insert(connection)
                    elif table_number == '5':
                        data_insert.charge_insert(connection)
                    elif table_number == '6':
                        data_insert.payment_insert(connection)

        except Error as e:
            print(e) '''


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
