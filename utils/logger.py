from datetime import datetime
from time import time

from os import mkdir, getcwd
from os.path import join as join_paths, exists


class Logger:
    def __init__(self, name: str) -> None:
        log_dir = join_paths(getcwd(), 'logs')
        if not exists(log_dir):
            mkdir(log_dir)

        date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.file_name = join_paths(log_dir, f'{date}_{name}.csv')

    def log(self,message: str, action: lambda: str) -> str:
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        start_time = time()
        result = action()
        end_time = time()
        
        duration = (end_time - start_time)*1000

        with open(self.file_name, 'a') as f:
            f.write(f'{date}; {duration}; {message}; {result}\n')
        
        return result
