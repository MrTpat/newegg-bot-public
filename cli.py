import click
from newegg.job import JobQueue
from newegg.logger import DebugLogger
import atexit

@click.command()
@click.argument('jobs_config_file')
@click.option('--real/--test', type=bool, default=False)

def run(jobs_config_file: str, real: bool) -> None:
   queue = JobQueue.from_config_file(jobs_config_file)
   queue.set_real(real)
   queue.run()

if __name__ == "__main__":
    atexit.register(DebugLogger.save_log_to_file)
    run()
