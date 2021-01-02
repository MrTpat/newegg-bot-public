from .communicator import NeweggCommunicator
from .profiles import BillingProfile
from .profiles import ProductProfile
from .profiles import SettingsProfile
from .util import universal_function_limiter
from .util import gather_cookies
from .logger import Logger
from enum import Enum
from typing import Optional
import threading
import json


class JobQueue:
    def __init__(self, jobs: list) -> None:
        self.jobs = jobs
        self.real = False

    def set_real(self, real: bool) -> None:
        self.real = real

    def run(self) -> None:
        for job in self.jobs:
            job.real = self.real
            job.start()

    @staticmethod
    def from_config_file(fl: str):
        try:
            # print(os.getcwd())
            json_file = open(f"configs/{fl}")
            jobs_array = json.load(json_file)
            json_file.close()
            jobs = []
            for j in jobs_array:
                jobs.append(
                    Job(
                        j["billing_config_file"],
                        j["product_config_file"],
                        j["settings_config_file"],
                        j["job_name"],
                        False,
                        j["attempts"],
                    )
                )
            return JobQueue(jobs)
        except Exception as e:
            Logger("[Jobs Profile] ").handle_err(e)


class State(Enum):
    failed = -1
    unstarted = 0
    trying_to_add_to_cart = 1
    added_to_cart = 2
    checking_cart_is_not_empty = 3
    cart_is_not_empty = 4
    generating_session_id = 5
    generated_session_id = 6
    getting_transaction_number = 7
    got_transaction_number = 8
    submitting_card_info = 9
    submitted_card_info = 10
    validating_address = 11
    validated_address = 12
    submitting_order = 13
    submitted_order = 14


class JobState:
    def __init__(self, job_instance):
        self.state: State = State.unstarted
        self.transaction_number: Optional[int] = None
        self.session_id: Optional[str] = None
        self.job_instance: Job = job_instance
        self.logger: Logger = self.job_instance.logger

    def reset(self):
        self.kill()
        self.state = State.unstarted

    def update(self, transaction_number: Optional[int], session_id: Optional[str]):
        self.state = State(self.state.value + 1)
        self.logger.log_info(f"New State: {self.state.name}")
        self.transaction_number = transaction_number
        self.session_id = session_id

    def kill(self):
        self.logger.log_important(f"Killed @ {self.state.name}")
        self.state = State.failed
        self.transaction_number = None
        self.session_id = None

    def is_alive(self):
        return self.state != State.failed

    def died(self):
        return not self.is_alive()


class Job(threading.Thread):
    def __init__(
        self,
        billing_config_file: str,
        product_config_file: str,
        settings_config_file: str,
        job_name: str,
        real: bool,
        attempts: int,
    ) -> None:
        self.billing_profile: BillingProfile = BillingProfile.from_config_file(
            billing_config_file
        )
        self.product_profile: ProductProfile = ProductProfile.from_config_file(
            product_config_file
        )
        self.settings_profile: SettingsProfile = SettingsProfile.from_config_file(
            settings_config_file
        )
        self.job_name: str = job_name
        self.real: bool = real
        self.attempts: int = attempts
        self.cookies: dict = gather_cookies(self.settings_profile.cookie_file)
        self.logger: Logger = Logger(f"[Job: {job_name}] ")
        threading.Thread.__init__(self)

    def run(self) -> None:
        self.logger.log_important(
            f"Running {self.attempts} attempts of job: {self.job_name}"
        )
        if universal_function_limiter(self.run_once, self.attempts, {}, False):
            self.logger.log_success(f"Job {self.job_name} succeeded!")
        else:
            self.logger.log_err(f"Job {self.job_name} failed!")

    def run_once(self) -> bool:
        self.logger.log_important(f"Running attempt of job: {self.job_name}")
        if self.real:
            finalState = self.run_real_job(self.cookies)
        else:
            finalState = self.run_test_job(self.cookies)

        if finalState.died():
            self.logger.log_important(f"Died")
        else:
            self.logger.log_important(f"Finished")

        return finalState.is_alive()

    def run_test_job(self, cookies: dict) -> JobState:
        communicator: NeweggCommunicator = NeweggCommunicator(
            cookies, self.settings_profile.timeout
        )
        return self.run_test_subroutine(communicator)

    def run_real_job(self, cookies: dict) -> JobState:
        communicator: NeweggCommunicator = NeweggCommunicator(
            cookies, self.settings_profile.timeout
        )
        return self.run_real_subroutine(communicator)

    def run_test_subroutine(self, communicator: NeweggCommunicator) -> JobState:
        state: JobState = JobState(self)
        self.add_to_cart(communicator, state)
        self.cart_is_not_empty(communicator, state)
        self.gen_session_id(communicator, state)
        self.get_transaction_number(communicator, state)
        self.submit_card_info(communicator, state)
        self.validate_address(communicator, state)
        return state

    def run_real_subroutine(self, communicator: NeweggCommunicator) -> JobState:
        state: JobState = JobState(self)
        self.add_to_cart(communicator, state)
        self.cart_is_not_empty(communicator, state)
        self.gen_session_id(communicator, state)
        self.get_transaction_number(communicator, state)
        self.submit_card_info(communicator, state)
        self.validate_address(communicator, state)
        self.submit_order(communicator, state)
        return state

    def add_to_cart(self, communicator: NeweggCommunicator, state: JobState) -> None:
        atc_limit = self.settings_profile.atc_limit
        if state.is_alive():
            state.update(state.transaction_number, state.session_id)
            if not universal_function_limiter(
                communicator.add_to_cart,
                atc_limit,
                self.product_profile.__dict__,
                False,
            ):
                state.kill()
            else:
                state.update(state.transaction_number, state.session_id)

    def cart_is_not_empty(
        self, communicator: NeweggCommunicator, state: JobState
    ) -> None:
        cis_limit = self.settings_profile.cis_limit
        if state.is_alive():
            state.update(state.transaction_number, state.session_id)
            if not universal_function_limiter(
                communicator.cart_is_not_empty,
                cis_limit,
                {},
                False,
            ):
                state.kill()
            else:
                state.update(state.transaction_number, state.session_id)

    def gen_session_id(self, communicator: NeweggCommunicator, state: JobState) -> None:
        if state.is_alive():
            state.update(state.transaction_number, state.session_id)
            gen_session_id_limit = self.settings_profile.gen_session_id_limit
            val = universal_function_limiter(
                communicator.gen_session_id,
                gen_session_id_limit,
                self.product_profile.__dict__,
                None,
            )
            if val is None:
                state.kill()
            else:
                state.update(state.transaction_number, val)

    def get_transaction_number(
        self, communicator: NeweggCommunicator, state: JobState
    ) -> None:
        if state.is_alive():
            state.update(state.transaction_number, state.session_id)
            get_transaction_number_limit = self.settings_profile.gen_session_id_limit
            val = universal_function_limiter(
                communicator.get_transaction_number,
                get_transaction_number_limit,
                {"session_id": state.session_id},
                None,
            )
            if val is None:
                return state.kill()
            else:
                state.update(val, state.session_id)

    def submit_card_info(
        self, communicator: NeweggCommunicator, state: JobState
    ) -> None:
        if state.is_alive():
            state.update(state.transaction_number, state.session_id)
            submit_card_info_limit = self.settings_profile.submit_card_info_limit
            data = state.__dict__.copy()
            data.update(self.billing_profile.__dict__)
            if not universal_function_limiter(
                communicator.submit_card_info, submit_card_info_limit, data, False
            ):
                state.kill()
            else:
                state.update(state.transaction_number, state.session_id)

    def validate_address(
        self, communicator: NeweggCommunicator, state: JobState
    ) -> None:
        if state.is_alive():
            state.update(state.transaction_number, state.session_id)
            address_validate_params = state.__dict__.copy()
            address_validate_params.update(self.billing_profile.__dict__)
            validate_address_limit = self.settings_profile.validate_address_limit
            if not universal_function_limiter(
                communicator.validate_address,
                validate_address_limit,
                address_validate_params,
                False,
            ):
                state.kill()
            else:
                state.update(state.transaction_number, state.session_id)

    def submit_order(self, communicator: NeweggCommunicator, state: JobState) -> None:
        if state.is_alive():
            state.update(state.transaction_number, state.session_id)
            submit_order_limit = self.settings_profile.submit_order_limit
            if not universal_function_limiter(
                communicator.submit_order, submit_order_limit, state.__dict__, False
            ):
                state.kill()
            else:
                state.update(state.transaction_number, state.session_id)
