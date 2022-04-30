from datetime import datetime


class Log:
    now = datetime.now()

    @staticmethod
    def save(text):
        with open(f'{str(Log.now)}', 'a') as log_file:
            log_file.write(text)
