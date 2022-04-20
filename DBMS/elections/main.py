from mysql.connector import connect, Error
from flask_cors import CORS
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from flask import Flask
from flask import request
import json
import actions
import requests
import information


class Server(object):

    def __init__(self):
        self.db = connect(
                    host="localhost",
                    user="bot_elections",
                    password="bkJIGj9Pid20",
                    database="elections",
            )

        self.app = Flask(__name__)
        CORS(self.app)

        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/election_commission_level/add', 'add_election_commission_level',
                              self.add_election_commission_level, methods=['POST'])
        self.app.add_url_rule('/election_commission_level/delete', 'delete_election_commission_level',
                              self.delete_election_commission_level, methods=['POST'])
        self.app.add_url_rule('/organizer/add', 'add_organizer',
                              self.add_organizer, methods=['POST'])
        self.app.add_url_rule('/organizer/delete', 'delete_organizer',
                              self.delete_organizer, methods=['POST'])
        self.app.add_url_rule('/organizer/change', 'change_organizers',
                              self.change_organizers, methods=['POST'])
        self.app.add_url_rule('/organizer/password', 'change_organizers_password',
                              self.change_organizers_password, methods=['POST'])
        self.app.add_url_rule('/observer/add', 'add_observer',
                              self.add_observer, methods=['POST'])
        self.app.add_url_rule('/observer/delete', 'delete_observer',
                              self.delete_observer, methods=['POST'])
        self.app.add_url_rule('/observer/change', 'change_observers',
                              self.change_observers, methods=['POST'])
        self.app.add_url_rule('/observer/password', 'change_observers_password',
                              self.change_observers_password, methods=['POST'])
        self.app.add_url_rule('/complaint/add', 'add_complaint',
                              self.add_complaint, methods=['POST'])
        self.app.add_url_rule('/complaint/delete', 'delete_complaint',
                              self.delete_complaint, methods=['POST'])
        self.app.add_url_rule('/complaint/change', 'change_complaint_message',
                              self.change_complaint_message, methods=['POST'])
        self.app.add_url_rule('/complaint/accept', 'accept_complaint',
                              self.accept_complaint, methods=['POST'])
        self.app.add_url_rule('/complaint/resolve', 'resolve_complaint',
                              self.resolve_complaint, methods=['POST'])
        self.app.add_url_rule('/training/add', 'add_training',
                              self.add_training, methods=['POST'])
        self.app.add_url_rule('/training/delete', 'delete_training',
                              self.delete_training, methods=['POST'])
        self.app.add_url_rule('/training/change', 'change_training',
                              self.change_training, methods=['POST'])
        self.app.add_url_rule('/training/registration', 'register_for_training',
                              self.register_for_training, methods=['POST'])
        self.app.add_url_rule('/training/un-registration', 'remove_from_training',
                              self.remove_from_training, methods=['POST'])
        self.app.add_url_rule('/election_commission/add', 'add_election_commission',
                              self.add_election_commission, methods=['POST'])
        self.app.add_url_rule('/election_commission/delete', 'delete_election_commission',
                              self.delete_election_commission, methods=['POST'])
        self.app.add_url_rule('/election_commission/change', 'change_election_commission',
                              self.change_election_commission, methods=['POST'])
        self.app.add_url_rule('/observation/add', 'assign_observer',
                              self.assign_observer, methods=['POST'])
        self.app.add_url_rule('/observation/delete', 'reassign_observer',
                              self.reassign_observer, methods=['POST'])
        self.app.add_url_rule('/party/add', 'add_party',
                              self.add_party, methods=['POST'])
        self.app.add_url_rule('/party/delete', 'delete_party',
                              self.delete_party, methods=['POST'])
        self.app.add_url_rule('/candidate/add', 'add_candidate',
                              self.add_candidate, methods=['POST'])
        self.app.add_url_rule('/candidate/delete', 'delete_candidate',
                              self.delete_candidate, methods=['POST'])
        self.app.add_url_rule('/results/add', 'add_results',
                              self.add_results, methods=['POST'])
        self.app.add_url_rule('/results/change', 'change_results',
                              self.change_results, methods=['POST'])
        self.app.add_url_rule('/results/confirm', 'confirm_results',
                              self.confirm_results, methods=['POST'])

        self.app.add_url_rule('/results/total', 'total_results',
                              self.total_results, methods=['GET'])
        self.app.add_url_rule('/results/candidate', 'results_by_candidate',
                              self.results_by_candidate, methods=['GET'])
        self.app.add_url_rule('/observer/profile', 'observer_profile',
                              self.observer_profile, methods=['GET'])
        self.app.add_url_rule('/organizer/profile', 'organizer_profile',
                              self.organizer_profile, methods=['GET'])
        self.app.add_url_rule('/organizer/training', 'organizer_training',
                              self.organizer_training, methods=['GET'])
        self.app.add_url_rule('/observer/training', 'observer_training',
                              self.observer_training, methods=['GET'])
        self.app.add_url_rule('/participant/training', 'participant_training',
                              self.participant_training, methods=['GET'])
        self.app.add_url_rule('/observation/total', 'total_observation',
                              self.total_observation, methods=['GET'])
        self.app.add_url_rule('/election_commission/lost', 'lost_election_commission',
                              self.lost_election_commission, methods=['GET'])
        self.app.add_url_rule('/observer/lost', 'lost_observer',
                              self.lost_observer, methods=['GET'])
        self.app.add_url_rule('/candidate/list', 'candidates_list',
                              self.candidates_list, methods=['GET'])
        self.app.add_url_rule('/education_level/list', 'dic_education_level',
                              self.dic_education_level, methods=['GET'])
        self.app.add_url_rule('/election_commission/list', 'dic_election_commission',
                              self.dic_election_commission, methods=['GET'])
        self.app.add_url_rule('/party/list', 'dic_party',
                              self.dic_party, methods=['GET'])
        self.app.add_url_rule('/complaint/total', 'total_complaints',
                              self.total_complaints, methods=['GET'])
        self.app.add_url_rule('/observer/complaint', 'observer_complaints',
                              self.observer_complaints, methods=['GET'])
        self.app.add_url_rule('/complaint/one', 'one_complaint',
                              self.one_complaint, methods=['GET'])

    def one_complaint(self):
        complaint_id = request.args.get('complaint_id', default=1, type=int)
        return json.dumps(information.one_complaint(self.db, complaint_id))

    def observer_complaints(self):
        person_rk = request.args.get('person_rk', default=1, type=int)
        return json.dumps(information.observer_complaints(self.db, person_rk))

    def total_complaints(self):
        return json.dumps(information.total_complaints(self.db))

    def dic_party(self):
        return json.dumps(information.dic_party(self.db))

    def dic_election_commission(self):
        return json.dumps(information.dic_election_commission(self.db))

    def dic_education_level(self):
        return json.dumps(information.dic_education_level(self.db))

    def candidates_list(self):
        return json.dumps(information.candidates_list(self.db))

    def lost_observer(self):
        return json.dumps(information.lost_observer(self.db))

    def lost_election_commission(self):
        return json.dumps(information.lost_election_commission(self.db))

    def total_observation(self):
        return json.dumps(information.total_observation(self.db))

    def participant_training(self):
        person_rk = request.args.get('person_rk', default=1, type=int)
        return json.dumps(information.participant_training(self.db, person_rk))

    def observer_training(self):
        person_rk = request.args.get('person_rk', default=1, type=int)
        return json.dumps(information.observer_training(self.db, person_rk))

    def organizer_training(self):
        person_rk = request.args.get('person_rk', default=1, type=int)
        return json.dumps(information.organizer_training(self.db, person_rk))

    def organizer_profile(self):
        person_rk = request.args.get('person_rk', default=1, type=int)
        return json.dumps(information.organizer_profile(self.db, person_rk))

    def observer_profile(self):
        person_rk = request.args.get('person_rk', default=1, type=int)
        return json.dumps(information.observer_profile(self.db, person_rk))

    def results_by_candidate(self):
        candidate_rk = request.args.get('candidate_rk', default=1, type=int)
        return json.dumps(information.results_by_candidate(self.db, candidate_rk))

    def total_results(self):
        return json.dumps(information.total_results(self.db))

    @staticmethod
    def index(self):
        return 'Hello, World!'

    def add_election_commission_level(self):
        data = request.get_json(force=True)
        print(data)
        args = []
        try:
            for el in requests.DicElectionCommission.pattern:
                args.append(str(data[el]))
        except KeyError as ke:
            print(ke)
            return str(ke), 500
        try:
            actions.add_election_commission_level(self.db, args)
        except Error as er:
            print(er)
            return str(er), 500
        return 'success', 201

    def delete_election_commission_level(self):
        data = request.get_json()
        print(data)
        try:
            actions.delete_election_commission_level(self.db, data['election_commission_cd'])
        except Error as er:
            print(er)
            return str(er), 500
        return 'success', 201

    def add_organizer(self):
        data = request.get_json()
        print(data)
        args = []
        try:
            for el in requests.Person.pattern[1:]:
                args.append(str(data[el]))
        except KeyError as ke:
            print(ke)
            return str(ke), 500
        try:
            actions.add_organizer(self.db, args)
        except Error as er:
            print(er)
            return str(er), 500
        return 'success', 201

    def delete_organizer(self):
        data = request.get_json()
        print(data)
        try:
            actions.delete_organizer(self.db, data['person_rk'])
        except Error as er:
            print(er)
            return str(er), 500
        return 'success', 201

    def change_organizers(self):
        data = request.get_json()
        print(data)
        args = []
        for el in requests.Person.pattern:
            try:
                args.append(str(data[el]))
            except KeyError:
                args.append(None)
        try:
            actions.change_organizers(self.db, args)
        except Error as er:
            print(er)
            return str(er), 500
        return 'success', 201

    def change_organizers_password(self):
        data = request.get_json()
        print(data)
        try:
            actions.change_organizers_password(self.db, data['login'], data['password'])
        except Error as er:
            print(er)
            return str(er), 500
        return 'success', 201

    def add_observer(self):
        data = request.get_json()
        print(data)
        args = []
        try:
            for el in requests.Person.pattern:
                args.append(str(data[el]))
        except KeyError as ke:
            print(ke)
            return str(ke), 500
        try:
            actions.add_observer(self.db, args)
        except Error as er:
            print(er)
            return str(er), 500
        return 'success', 201

    def delete_observer(self):
        data = request.get_json()
        print(data)
        try:
            actions.delete_observer(self.db, data['person_rk'])
        except Error as er:
            print(er)
            return str(er), 500
        return 'success', 201

    def change_observers(self):
        data = request.get_json()
        print(data)
        args = []
        for el in requests.Person.pattern:
            try:
                args.append(data[el])
            except KeyError:
                args.append(None)
        try:
            actions.change_observers(self.db, args)
        except Error as er:
            print(er)
            return str(er), 500
        return 'success', 201

    def change_observers_password(self):
        data = request.get_json()
        print(data)
        try:
            actions.change_organizers_password(self.db, data['login'], data['password'])
        except Error as er:
            print(er)
            return str(er), 500
        return 'success', 201

    def add_complaint(self):
        data = request.get_json()
        print(data)
        args = []
        try:
            for el in requests.Complaint.pattern[1:]:
                args.append(str(data[el]))
        except KeyError as ke:
            print(ke)
            return str(ke), 500
        try:
            actions.add_complaint(self.db, args)
        except Error as er:
            print(er)
            return str(er), 500
        return 'success', 201

    def delete_complaint(self):
        data = request.get_json()
        print(data)
        try:
            actions.delete_complaint(self.db, data['complaint_id'])
        except Error as er:
            print(er)
            return str(er), 500
        return 'success', 201

    def change_complaint_message(self):
        data = request.get_json()
        print(data)
        args = []
        for el in requests.Complaint.pattern:
            try:
                args.append(data[el])
            except KeyError:
                args.append(None)
        try:
            actions.change_complaint_message(self.db, args)
        except Error as er:
            print(er)
            return str(er), 500
        return 'success', 201

    def accept_complaint(self):
        data = request.get_json()
        print(data)
        args = []
        for el in requests.Complaint.pattern:
            try:
                args.append(data[el])
            except KeyError:
                args.append(None)
        try:
            actions.accept_complaint(self.db, args)
        except Error as er:
            print(er)
            return str(er), 500
        return 'success', 201

    def resolve_complaint(self):
        data = request.get_json()
        print(data)
        args = []
        for el in requests.Complaint.pattern:
            try:
                args.append(data[el])
            except KeyError:
                args.append(None)
        try:
            actions.resolve_complaint(self.db, args)
        except Error as er:
            print(er)
            return str(er), 500
        return 'success', 201

    def add_training(self):
        data = request.get_json()
        print(data)
        args = []
        try:
            for el in requests.Education.pattern[1:]:
                args.append(str(data[el]))
        except KeyError as ke:
            print(ke)
            return str(ke), 500
        try:
            actions.add_training(self.db, args)
        except Error as er:
            print(er)
            return str(er), 500
        return 'success', 201

    def delete_training(self):
        data = request.get_json()
        print(data)
        try:
            actions.delete_training(self.db, data['education_id'])
        except Error as er:
            print(er)
            return str(er), 500
        return 'success', 201

    def change_training(self):
        data = request.get_json()
        print(data)
        args = []
        for el in requests.Education.pattern:
            try:
                args.append(data[el])
            except KeyError:
                args.append(None)
        try:
            actions.change_training(self.db, args)
        except Error as er:
            print(er)
            return str(er), 500
        return 'success', 201

    def register_for_training(self):
        data = request.get_json()
        print(data)
        args = []
        try:
            for el in requests.Participant.pattern:
                args.append(str(data[el]))
        except KeyError as ke:
            print(ke)
            return str(ke), 500
        try:
            actions.register_for_training(self.db, args)
        except Error as er:
            print(er)
            return str(er), 500
        return 'success', 201

    def remove_from_training(self):
        data = request.get_json()
        print(data)
        try:
            actions.remove_from_training(self.db, data['education_id'], data['observer_rk'])
        except Error as er:
            print(er)
            return str(er), 500
        return 'success', 201

    def add_election_commission(self):
        data = request.get_json()
        print(data)
        args = []
        try:
            for el in requests.ElectionCommission.pattern[1:]:
                args.append(str(data[el]))
        except KeyError as ke:
            print(ke)
            return str(ke), 500
        try:
            actions.add_election_commission(self.db, args)
        except Error as er:
            print(er)
            return str(er), 500
        return 'success', 201

    def delete_election_commission(self):
        data = request.get_json()
        print(data)
        try:
            actions.delete_election_commission(self.db, data['election_commission_rk'])
        except Error as er:
            print(er)
            return str(er), 500
        return 'success', 201

    def change_election_commission(self):
        data = request.get_json()
        print(data)
        args = []
        for el in requests.ElectionCommission.pattern:
            try:
                args.append(data[el])
            except KeyError:
                args.append(None)
        try:
            actions.change_election_commission(self.db, args)
        except Error as er:
            print(er)
            return str(er), 500
        return 'success', 201

    def assign_observer(self):
        data = request.get_json()
        print(data)
        args = []
        try:
            for el in requests.Observation.pattern[1:]:
                args.append(str(data[el]))
        except KeyError as ke:
            print(ke)
            return str(ke), 500
        try:
            actions.assign_observer(self.db, args)
        except Error as er:
            print(er)
            return str(er), 500
        return 'success', 201

    def reassign_observer(self):
        data = request.get_json()
        print(data)
        try:
            actions.reassign_observer(self.db, data['observation_id'])
        except Error as er:
            print(er)
            return str(er), 500
        return 'success', 201

    def add_party(self):
        data = request.get_json()
        print(data)
        args = []
        try:
            for el in requests.DicParty.pattern:
                args.append(str(data[el]))
        except KeyError as ke:
            print(ke)
            return str(ke), 500
        try:
            actions.add_party(self.db, args)
        except Error as er:
            print(er)
            return str(er), 500
        return 'success', 201

    def delete_party(self):
        data = request.get_json()
        print(data)
        try:
            actions.delete_party(self.db, data['party_cd'])
        except Error as er:
            print(er)
            return str(er), 500
        return 'success', 201

    def add_candidate(self):
        data = request.get_json()
        print(data)
        args = []
        try:
            for el in requests.Candidate.pattern[1:]:
                args.append(str(data[el]))
        except KeyError as ke:
            print(ke)
            return str(ke), 500
        try:
            actions.add_candidate(self.db, args)
        except Error as er:
            print(er)
            return str(er), 500
        return 'success', 201

    def delete_candidate(self):
        data = request.get_json()
        print(data)
        try:
            actions.delete_candidate(self.db, data['candidate_rk'])
        except Error as er:
            print(er)
            return str(er), 500
        return 'success', 201

    def add_results(self):
        data = request.get_json()
        print(data)
        args = []
        try:
            for el in requests.Results.pattern:
                args.append(str(data[el]))
        except KeyError as ke:
            print(ke)
            return str(ke), 500
        try:
            actions.add_results(self.db, args)
        except Error as er:
            print(er)
            return str(er), 500
        return 'success', 201

    def change_results(self):
        data = request.get_json()
        print(data)
        args = []
        for el in requests.Results.pattern:
            try:
                args.append(data[el])
            except KeyError:
                args.append(None)
        try:
            actions.change_results(self.db, args)
        except Error as er:
            print(er)
            return str(er), 500
        return 'success', 201

    def confirm_results(self):
        data = request.get_json()
        print(data)
        args = []
        for el in requests.Results.pattern:
            try:
                args.append(data[el])
            except KeyError:
                args.append(None)
        try:
            actions.confirm_results(self.db, args)
        except Error as er:
            print(er)
            return str(er), 500
        return 'success', 201


    def __del__(self):
        self.db.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('PyCharm')

    srv = Server()

    srv.app.run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
