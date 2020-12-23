from communicator import NeweggCommunicator
from profiles import BillingProfile
from profiles import ProductProfile
from profiles import SettingsProfile
from util import universal_function_limiter

class Job:
    def __init__(self, billing_config_file: str, product_config_file: str, settings_config_file: str) -> None:
        self.billing_profile: BillingProfile = BillingProfile.from_config_file(billing_config_file)
        self.product_profile: ProductProfile = ProductProfile.from_config_file(product_config_file)
        self.settings_profile: SettingsProfile = SettingsProfile.from_config_file(settings_config_file)

    def run_test_job(self, cookies: dict):
        communicator: NeweggCommunicator = NeweggCommunicator(cookies, self.settings_profile.timeout)
        self.run_test_subroutine(communicator)

    def run_real_job(self, cookies: dict):
        communicator: NeweggCommunicator = NeweggCommunicator(cookies, self.settings_profile.timeout)
        self.run_subroutine(communicator)

    def run_test_subroutine(self, communicator: NeweggCommunicator) -> bool:
        atc_limit = self.settings_profile.atc_limit
        gen_session_id_limit = self.settings_profile.gen_session_id_limit
        get_transaction_number_limit = self.settings_profile.gen_session_id_limit
        submit_card_info_limit = self.settings_profile.submit_card_info_limit
        validate_address_limit = self.settings_profile.validate_address_limit
        cvv = self.billing_profile.cvv
        if universal_function_limiter(communicator.add_to_cart, atc_limit, self.product_profile.__dict__, False):
            print('Added to cart')
            session_id = universal_function_limiter(communicator.gen_session_id, gen_session_id_limit, self.product_profile.__dict__, None)
            if session_id is None:
                return False
            print(session_id)
            transaction_number = universal_function_limiter(communicator.get_transaction_number, get_transaction_number_limit, {'session_id': session_id}, None)
            if transaction_number is None:
                return False
            print(transaction_number)

            if universal_function_limiter(communicator.submit_card_info, submit_card_info_limit, {'transaction_number': transaction_number, 'cvv': cvv, 'session_id': session_id}, False):
                print('submitted card info')
                if universal_function_limiter(communicator.validate_address, validate_address_limit, self.product_profile.__dict__, False):
                    print('validated address')
            else:
                return False
        else:
            return False

    def run_real_subroutine(self, communicator: NeweggCommunicator) -> bool:
        return True

