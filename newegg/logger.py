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
        click.secho(s, fg='red', bold=True)

    def log_info(self, s: str) -> None:
        s = f'{self.pre_text}{s}'
        click.secho(s, fg='blue')

    def log_success(self, s: str) -> None:
        s = f'{self.pre_text}{s}'
        click.secho(s, fg='green', bold=True)

    def log_important(self, s:str) -> None:
        s = f'{self.pre_text}{s}'
        click.secho(s, fg='yellow', bold=True)

    def handle_err(self, e: Exception) -> None:
        self.log_err(str(e))
        exit(1)
