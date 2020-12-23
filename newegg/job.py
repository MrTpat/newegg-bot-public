from communicator import NeweggCommunicator
from profiles import BillingProfile
from profiles import ProductProfile
from profiles import SettingsProfile
from util import universal_function_limiter
from enum import Enum
from typing import Optional

class Job:
    class JobState:
        class State(Enum):
            failed = -1
            unstarted = 0
            trying_to_add_to_cart = 1
            added_to_cart = 2
            generating_session_id = 3
            generated_session_id = 4
            getting_transaction_number = 5
            got_transaction_number = 6
            submitting_card_info = 7
            submitted_card_info = 8
            validating_address = 9
            validated_address = 10
            completed = 11
        
        def __init__(self, communicator):
            self.state: self.State = self.State.unstarted
            self.transaction_number: Optional[int] = None
            self.session_id: Optional[str] = None
        
        def reset(self):
            self.state = State.unstarted
        def update(self, transaction_number: Optional[int], session_id: Optional[str]):
            self.state = self.State(self.state.value + 1)
            print(f'New State: {self.state.name}')
            self.transaction_number = transaction_number
            self.session_id = session_id
        def kill(self):
            print(f'killed @ {self.state.name}')
            self.state = self.State.failed
            self.transaction_number = None
            self.session_id = None
        def is_alive(self):
            return self.state != self.State.failed

    def __init__(self, billing_config_file: str, product_config_file: str, settings_config_file: str) -> None:
        self.billing_profile: BillingProfile = BillingProfile.from_config_file(billing_config_file)
        self.product_profile: ProductProfile = ProductProfile.from_config_file(product_config_file)
        self.settings_profile: SettingsProfile = SettingsProfile.from_config_file(settings_config_file)

    def run_test_job(self, cookies: dict):
        communicator: NeweggCommunicator = NeweggCommunicator(cookies, self.settings_profile.timeout)
        self.run_test_subroutine(communicator)

    def run_real_job(self, cookies: dict):
        communicator: NeweggCommunicator = NeweggCommunicator(cookies, self.settings_profile.timeout)
        self.run_real_subroutine(communicator)

    def run_test_subroutine(self, communicator: NeweggCommunicator) -> None:
        state: self.JobState = self.JobState(communicator)
        self.add_to_cart(communicator, state)
        self.gen_session_id(communicator, state)
        self.get_transaction_number(communicator, state)
        self.submit_card_info(communicator, state)
        self.validate_address(communicator, state)

    def run_real_subroutine(self, communicator: NeweggCommunicator) -> bool:
        return True

    def add_to_cart(self, communicator: NeweggCommunicator, state: JobState) -> None:
        atc_limit = self.settings_profile.atc_limit
        if state.is_alive():
            state.update(state.transaction_number, state.session_id)
            if not universal_function_limiter(communicator.add_to_cart, atc_limit, self.product_profile.__dict__, False):
                state.kill()
            else:
                state.update(state.transaction_number, state.session_id)

    def gen_session_id(self, communicator: NeweggCommunicator, state: JobState) -> None:
        if state.is_alive():
            state.update(state.transaction_number, state.session_id)
            gen_session_id_limit = self.settings_profile.gen_session_id_limit
            val = universal_function_limiter(communicator.gen_session_id, gen_session_id_limit, self.product_profile.__dict__, None)
            if val is None:
                state.kill()
            else:
                state.update(state.transaction_number, val)

    def get_transaction_number(self, communicator: NeweggCommunicator, state: JobState) -> None:
        if state.is_alive():
            state.update(state.transaction_number, state.session_id)
            get_transaction_number_limit = self.settings_profile.gen_session_id_limit
            val = universal_function_limiter(communicator.get_transaction_number, get_transaction_number_limit, {'session_id': state.session_id}, None)
            if val is None:
                return state.kill()
            else:
                state.update(val, state.session_id)
    
    def submit_card_info(self, communicator: NeweggCommunicator, state: JobState) -> None:
        if state.is_alive():
            state.update(state.transaction_number, state.session_id)
            submit_card_info_limit = self.settings_profile.submit_card_info_limit
            data = state.__dict__.copy()
            data.update(self.billing_profile.__dict__)
            if not universal_function_limiter(communicator.submit_card_info, submit_card_info_limit, data, False):
                state.kill()
            else:
                state.update(state.transaction_number, state.session_id)

    def validate_address(self, communicator: NeweggCommunicator, state: JobState) -> None:
        if state.is_alive():
            address_validate_params = self.billing_profile.__dict__.copy()
            address_validate_params.update(state.__dict__)
            validate_address_limit = self.settings_profile.validate_address_limit
            if universal_function_limiter(communicator.validate_address, validate_address_limit, address_validate_params, False):
                state.kill()
            else:
                state.update(state.transaction_number, state.session_id)
