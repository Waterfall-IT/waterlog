from colorama import Fore, Back, Style
from inspect  import stack
from typing   import Optional
from time     import time

from .methods import to_fixed


class LogLevel:
    DEBUG = 0
    INFO  = 1
    WARN  = 2
    ERROR = 3
    FATAL = 4


class Logger:

    _LEVEL_SCHEMA = {
        0: (Fore.LIGHTBLACK_EX,            'D', Fore.RESET),
        1: (Fore.LIGHTWHITE_EX,            'I', Fore.RESET),
        2: (Fore.LIGHTYELLOW_EX,           'W', Fore.RESET),
        3: (Fore.LIGHTRED_EX,              'E', Fore.RESET),
        4: (Fore.BLACK + Back.LIGHTRED_EX, 'F', Style.RESET_ALL)
    }

    def __init__(self, path: str, level: int = LogLevel.INFO) -> None:

        self.level = level
        self.start_time = time()
        self.file = open(path, 'a')

    def _write(self, file_message: str, stdout_message: Optional[str] = None) -> None:
        if stdout_message is None:
            stdout_message = file_message
        self.file.write(file_message)
        print(stdout_message, end = '')

    def _get_head(self, level: int, time_ndigits: int = 4, colors: bool = True) -> str:
        if colors:
            return f'{self._LEVEL_SCHEMA[level][0]}[{to_fixed(time() - self.start_time, time_ndigits)}] [{self._LEVEL_SCHEMA[level][1]}] '
        return f'[{to_fixed(time() - self.start_time, time_ndigits)}] [{self._LEVEL_SCHEMA[level][1]}] '
    
    def _get_tail(self, level: int, colors: bool = True) -> str:
        if colors:
            return self._LEVEL_SCHEMA[level][2] + '\n'
        return '\n'

    def log(self, level: int, message: str, forced: bool = False) -> None:
        if level >= self.level or forced:
            try:
                caller = stack()[2]
            except IndexError:
                caller = stack()[-1]
            self._write(
                self._get_head(level, False) + f'[{caller.function.replace('<module>', '<Bottom>')}@{caller.filename.split("/")[-1]}] ' + message + self._get_tail(level, False),
                self._get_head(level,  True) + f'[{caller.function.replace('<module>', '<Bottom>')}@{caller.filename.split("/")[-1]}] ' + message + self._get_tail(level,  True)
            )

    def debug(self, message: str) -> None:
        self.log(LogLevel.DEBUG, message)
    
    def info(self, message: str) -> None:
        self.log(LogLevel.INFO, message)

    def warn(self, message: str) -> None:
        self.log(LogLevel.WARN, message)

    def error(self, message: str) -> None:
        self.log(LogLevel.ERROR, message)

    def fatal(self, message: str) -> None:
        self.log(LogLevel.FATAL, message)

    def close(self) -> None:
        self.file.close()