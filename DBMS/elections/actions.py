import requests


def add_election_commission_level(connection, args):
    requests.DicElectionCommission.insert(connection, args)
    print('Success.')


def delete_election_commission_level(connection, election_commission_cd):
    requests.DicElectionCommission.delete(connection, [election_commission_cd])
    print('Success.')


def add_organizer(connection, args):
    requests.Person.insert(connection, args)
    print('Success.')


def delete_organizer(connection, person_rk):
    requests.Person.delete(connection, [person_rk])
    print('Success.')


def change_organizers(connection, args):
    requests.Person.update(connection, args)
    print('Success.')


def change_organizers_password(connection, login, password):
    person = requests.Person.select(connection, {'login': login, 'hash_password': password})
    person[8] = login
    person[9] = password
    requests.Person.update(connection, person)
    print('Success.')


def add_observer(connection, args):
    requests.Person.insert(connection, args)
    print('Success.')


def delete_observer(connection, person_rk):
    requests.Person.delete(connection, [person_rk])
    print('Success.')


def change_observers(connection, args):
    requests.Person.update(connection, args)
    print('Success.')


def change_observers_password(connection, login, password):
    person = requests.Person.select(connection, {'login': login, 'hash_password': password})
    person[8] = login
    person[9] = password
    requests.Person.update(connection, person)
    print('Success.')


def add_complaint(connection, args):
    requests.Complaint.insert(connection, args)
    print('Success.')


def delete_complaint(connection, complaint_id):
    requests.Complaint.delete(connection, [complaint_id])
    print('Success.')


def change_complaint_message(connection, args):
    requests.Complaint.update(connection, args)
    print('Success.')


def accept_complaint(connection, args):
    requests.Complaint.update(connection, args)
    print('Success.')


def resolve_complaint(connection, args):
    requests.Complaint.update(connection, args)
    print('Success.')


def add_training(connection, args):
    requests.Education.insert(connection, args)
    print('Success.')


def delete_training(connection, education_id):
    requests.Education.delete(connection, [education_id])
    print('Success.')


def change_training(connection, args):
    requests.Education.update(connection, args)
    print('Success.')


def register_for_training(connection, args):
    requests.Participant.insert(connection, args)
    print('Success.')


def remove_from_training(connection, education_id, observer_rk):
    requests.Participant.delete(connection, [observer_rk, education_id])
    print('Success.')


def add_election_commission(connection, args):
    requests.ElectionCommission.insert(connection, args)
    print('Success.')


def delete_election_commission(connection, election_commission_rk):
    requests.ElectionCommission.delete(connection, [election_commission_rk])
    print('Success.')


def change_election_commission(connection, args):
    requests.ElectionCommission.update(connection, args)
    print('Success.')


def assign_observer(connection, args):
    requests.Observation.insert(connection, args)
    print('Success.')


def reassign_observer(connection, observation_id):
    requests.Observation.delete(connection, [observation_id])
    print('Success.')


def add_party(connection, args):
    requests.DicParty.insert(connection, args)
    print('Success.')


def delete_party(connection, party_cd):
    requests.DicParty.delete(connection, [party_cd])
    print('Success.')


def add_candidate(connection, args):
    requests.Candidate.insert(connection, args)
    print('Success.')


def delete_candidate(connection, candidate_rk):
    requests.Candidate.delete(connection, [candidate_rk])
    print('Success.')


def add_results(connection, args):
    requests.Results.insert(connection, args)
    print('Success.')


def change_results(connection, args):
    requests.Results.update(connection, args)
    print('Success.')


def confirm_results(connection, args):
    requests.Results.update(connection, args)
    print('Success.')
