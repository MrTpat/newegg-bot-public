import json
from .logger import Logger


class BillingProfile:
    def __init__(self, name: str, phone: str, address: str, zip_code: str, state: str, city: str, cvv: str, country: str, country_long: str, card_provider:  str) -> None:
        self.name: str = name
        self.phone: str = phone
        self.address: str = address
        self.zip_code: str = zip_code
        self.state: str = state
        self.city: str = city
        self.cvv: str = cvv
        self.country: str = country
        self.country_long: str = country_long
        self.card_provider: str = card_provider

    @staticmethod
    def from_dict(d: dict):
        try:
            name = d['name']
            phone = d['phone']
            address = d['address']
            zip_code = d['zip_code']
            state = d['state']
            city = d['city']
            cvv = d['city']
            country = d['country']
            country_long = d['country_long']
            card_provider = d['card_provider']
            return BillingProfile(name, phone, address, zip_code, state, city, cvv, country, country_long, card_provider)
        except Exception as e:
            Logger.handle_err(e)
        
    @staticmethod
    def from_config_file(fl: str):
        try:
            json_file = open(f'configs/{fl}')
            j = json.load(json_file)
            json_file.close()
            return BillingProfile.from_dict(j)
        except Exception as e:
            Logger.handle_err(e)
        
class ProductProfile:
    def __init__(self, p_id: str, s_id: str, is_combo: bool) -> None:
        self.p_id = p_id
        self.s_id = s_id
        self.is_combo = is_combo

    @staticmethod
    def from_dict(d: dict):
        try:
            p_id = d['p_id']
            s_id = d['s_id']
            is_combo = d['is_combo']
            return ProductProfile(p_id, s_id, is_combo)
        except Exception as e:
            Logger.handle_err(e)
        
    @staticmethod
    def from_config_file(fl: str):
        try:
            json_file = open(f'configs/{fl}')
            j = json.load(json_file)
            json_file.close()
            return ProductProfile.from_dict(j)
        except Exception as e:
            Logger.handle_err(e)

class SettingsProfile:
    def __init__(self, timeout: int, atc_limit: int, gen_session_id_limit: int, get_transaction_number_limit: int, submit_card_info_limit: int, validate_address_limit: int, cookie_file: str, submit_order_limit: int) -> None:
        self.timeout: int = timeout
        self.atc_limit: int = atc_limit
        self.gen_session_id_limit: int = gen_session_id_limit
        self.get_transaction_number_limit: int = get_transaction_number_limit
        self.submit_card_info_limit: int = submit_card_info_limit
        self.validate_address_limit: int = validate_address_limit
        self.submit_order_limit: int = submit_order_limit
        self.cookie_file: str = cookie_file

    @staticmethod
    def from_dict(d: dict):
        try:
            timeout = d['timeout']
            atc_limit = d['atc_limit']
            gen_session_id_limit = d['gen_session_id_limit']
            get_transaction_number_limit = d['get_transaction_number_limit']
            submit_card_info_limit = d['submit_card_info_limit']
            validate_address_limit = d['validate_address_limit']
            cookie_file = d['cookie_file']
            submit_order_limit = d['submit_order_limit']
            return SettingsProfile(timeout, atc_limit, gen_session_id_limit, get_transaction_number_limit, submit_card_info_limit, validate_address_limit, cookie_file, submit_order_limit)
        except Exception as e:
            Logger.handle_err(e)
        
    @staticmethod
    def from_config_file(fl: str):
        try:
            json_file = open(f'configs/{fl}')
            j = json.load(json_file)
            json_file.close()
            return SettingsProfile.from_dict(j)
        except Exception as e:
            Logger.handle_err(e)
