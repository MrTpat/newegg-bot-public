import click
from typing import Optional

class Logger:

    def __init__(self, pre_text: Optional[str] = None) -> None:
        self.pre_text: Optional[str] = pre_text
        if self.pre_text is None:
            self.pre_text = ''
        click.clear()
        
    
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
    lines: list = []

    @staticmethod
    def log(s: str) -> None:
        DebugLogger.lines.append(s)

    @staticmethod
    def log_err(e: Exception) -> None:
        DebugLogger.log(str(e))

    @staticmethod
    def save_log_to_file() -> None:
        from datetime import datetime
        import os
        if not os.path.exists('./logs'):
            os.makedirs('./logs')
        try:
            now = datetime.now()
            str_date = now.strftime("%m_%d_%Y_%H_%M_%S")
            f = open(f'logs/{str_date}', 'w')
            DebugLogger.lines.append('') #prevents no newline at EOF
            string_to_write: str = '\n'.join(DebugLogger.lines)
            f.write(string_to_write)
            f.close()
        except Exception as e:
            Logger().handle_err(e)

