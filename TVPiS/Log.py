import datetime


now = datetime.datetime.now()


def save(text):
    with open(f'logs\\{now.strftime("%Y-%m-%d_%H-%M-%S")}.txt', 'a') as log_file:
        log_file.write(f'{text}\n')
