import click
from typing import Optional
from .util import ensure_dir_exists
import logging

class Logger:

    def __init__(self, pre_text: Optional[str] = None) -> None:
        self.pre_text: Optional[str] = pre_text
        if self.pre_text is None:
            self.pre_text = ''
    
    def log_err(self, s: str) -> None:
        s = f'{self.pre_text}{s}'
        DebugLogger.log(s)
        click.secho(s, fg='red', bold=True)

    def log_info(self, s: str) -> None:
        s = f'{self.pre_text}{s}'
        DebugLogger.log(s)
        click.secho(s, fg='blue')

    def log_success(self, s: str) -> None:
        s = f'{self.pre_text}{s}'
        DebugLogger.log(s)
        click.secho(s, fg='green', bold=True)

    def log_important(self, s:str) -> None:
        s = f'{self.pre_text}{s}'
        DebugLogger.log(s)
        click.secho(s, fg='yellow', bold=True)

    def handle_err(self, e: Exception) -> None:
        self.log_err(str(e))
        DebugLogger.log_err(e)
        exit(1)

class DebugLogger:
    from datetime import datetime
    ensure_dir_exists('./logs')
    logging.basicConfig(filename=f'./logs/{datetime.now().strftime("%m_%d_%Y_%H_%M_%S")}', filemode='w', level=0)

    @staticmethod
    def log(s: str) -> None:
        logging.info(s)

    @staticmethod
    def log_err(e: Exception) -> None:
        DebugLogger.log(str(e))
