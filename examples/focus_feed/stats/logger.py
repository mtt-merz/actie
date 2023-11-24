from datetime import datetime
from time import time

from os import mkdir, getcwd
from os.path import join as join_paths, exists


class Logger:
    def __init__(self, name: str) -> None:
        log_dir = join_paths(getcwd(), 'logs', name)
        if not exists(log_dir):
            mkdir(log_dir)

        date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.file_name = join_paths(log_dir, f'{date}.csv')

    def log(self, execute, args: dict) -> str:
        args['date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        start_time = time()
        result = execute()
        end_time = time()

        args['duration'] = (end_time - start_time)*1000
        args['result'] = result

        with open(self.file_name, 'a') as f:
            f.write(
                '; '.join([f'{k}={v}' for k, v in args.items()]) + '\n'
            )

        return result
