import requests
from base64 import standard_b64encode
import json
from typing import Optional

class NeweggCommunicator:
    def __init__(self, cookies, timeout) -> None:
        self.cookies = cookies
        self.timeout = timeout

    def add_to_cart(self, p_id: str, is_combo: bool, **kwargs) -> bool:
        url = 'https://secure.newegg.com/Shopping/AddtoCart.aspx?Submit=ADD&ItemList='
        if is_combo:
            url += 'Combo.'
        url += p_id
        try:
            req = requests.get(url, cookies=self.cookies, timeout=self.timeout)
            return p_id in req.url
        except:
            return False

    @staticmethod
    def get_default_headers(new_entries: dict) -> dict:
        defaults = {
            'authority': 'secure.newegg.com',
            'accept': 'application/json, text/plain, */*',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.57',
            'content-type': 'application/json',
            'origin': 'https://secure.newegg.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'accept-language': 'en-US,en;q=0.9'
            }
        defaults.update(new_entries)
        return defaults

    def gen_session_id(self, p_id: str, s_id: str, is_combo: bool, **kwargs) -> Optional[str]:
        def gen_data() -> dict:
            data = {'SaleType':1,'ItemGroup':1,'ItemNumber': s_id ,'OptionalInfos':[]}
            if is_combo:
                data['ItemGroup'] = 3
                data['ItemNumber'] = p_id
            encryptedBytes = standard_b64encode(str.encode(json.dumps(data))).decode()
            return {'ItemList': [{'ItemNumber': s_id, 'ItemKey': encryptedBytes, 'Quantity': 1}], 'Actions': []}

        url = 'https://secure.newegg.com/shop/api/CheckoutApi'
        headers = self.get_default_headers({'referer': 'https://secure.newegg.com/shop/cart'})
        data = gen_data()
        try:
            req = requests.post(url, headers=headers, data=data, cookies=self.cookies, timeout=self.timeout)
            if req.status_code != 200:
                return None
            json_res = req.json()
            return json_res['SessionID']
        except:
            return None

    def get_transaction_number(self, session_id: str, **kwargs) -> Optional[int]:
        url = 'https://secure.newegg.com/shop/api/InitOrderReviewApi'
        headers = self.get_default_headers({'x-sessionid': session_id, 'referer': f'https://secure.newegg.com/shop/checkout?sessionId={session_id}'})
        data = {'SessionID':session_id,'Actions':[{'ActionType':'AlterPanelStatus','JsonContent':json.dumps({'ActionType':'AlterPanelStatus','PanelStatus':{'ShippingAddress':'Done','DeliveryMethod':'Done','TaxID':'Done','Payment':'Todo'}})}],'EnableAsyncToken':True}
        try:
            req = requests.post(url, headers=headers, data=data, cookies=self.cookies, timeout=self.timeout)
            if req.status_code != 200:
                return None
            return req.json()['PaymentOption']['CreditCardList'][0]['TransactionNumber']
        except:
            return None

    def submit_card_info(self, transaction_number: int, cvv: str, session_id: str, **kwargs) -> bool:
        url = 'https://secure.newegg.com/shop/api/InitOrderReviewApi'
        headers = self.get_default_headers({'x-sessionid': session_id, 'referer': f'https://secure.newegg.com/shop/checkout?sessionId={session_id}'})
        data = {'SessionID':session_id,'Actions':[{'ActionType':'ConfirmPayment','JsonContent':json.dumps({'ActionType':'ConfirmPayment','Cvv2': cvv, 'TransactionNumber': transaction_number, 'PaytermsCode': 'Discover'})}],'EnableAsyncToken':True}
        try:
            req = requests.post(url, headers=headers, data=data, cookies=self.cookies, timeout=self.timeout)
            return req.status_code == 200
        except:
            return False

    def validate_address(self, transaction_number: int, name: str, phone: str, country: str, state: str, city: str, address: str, zip_code: str, country_long: str, session_id: str, **kwargs) -> bool:
        url = 'https://secure.newegg.com/shop/api/ValidateAddress'
        headers = self.get_default_headers({'x-sessionid': session_id, 'referer': f'https://secure.newegg.com/shop/checkout?sessionId={session_id}'})
        data = {'TransNumber': transaction_number, 'AddressLabel': 'Untitled', 'ContactWith': name, 'Phone': phone, 'Fax': '', 'Country': country, 'State': state, 'City': city, 'Address1': address, 'Address2': '', 'ZipCode': zip_code, 'IsDefault': False, 'DisplayLines': [address, f'{city}, {state} {zip_code}', country_long, phone], 'AddressVerifyMark': 'Verified', 'Email': None, 'DisableEmail': False, 'CompanyName': '', 'LanguageCode': None, 'IsSelected': False, 'SaveAddress': False, 'QASDisplayLines': [address, f'{city}, {state} {zip_code}', country_long]}
        try:
            req = requests.post(url, headers=headers, data=data, cookies=self.cookies, timeout=self.timeout)
            return req.status_code == 200
        except:
            return False

    def submit_order(self, session_id: str) -> bool:
        url = 'https://secure.newegg.com/shop/api/PlaceOrderApi'
        headers = self.get_default_headers({'x-sessionid': session_id, 'referer': 'https://secure.newegg.com/shop/checkout?sessionId={session_id}'})
        data = {'SessionID': session_id, 'IsAcceptNSCCAuth': False, 'SubscribeNewsletterFlag': False, 'CreactAccount': False, 'Password': '', 'MobileSubscribe': {}, 'LanguageCode': 'en-us', 'Cvv2': ''}
        try:
            req = requests.post(url, headers=headers, data=data, cookies=self.cookies, timeout=self.timeout)
            return req.status_code == 200
        except:
            return False
