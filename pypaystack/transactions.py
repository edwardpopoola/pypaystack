from .baseapi import BaseAPI
from . import utils
from .errors import InvalidDataError


class Transaction(BaseAPI):
    def getall(self, start_date=None, end_date=None, status=None, pagination=10):
        """
        Gets all your transactions

        args:
        pagination -- Count of data to return per call
        from: start date
        to: end date
        """
        url = self._url("/transaction/?perPage={}".format(pagination))
        url = url + "&status={}".format(status) if status else url
        url = url + "&from={}".format(start_date) if start_date else url
        url = url + "&to={}".format(end_date) if end_date else url

        return self._handle_request("GET", url)

    def getone(self, transaction_id):
        """
        Gets one customer with the given transaction id

        args:
        Transaction_id -- transaction we want to get
        """
        url = self._url("/transaction/{}/".format(transaction_id))
        return self._handle_request("GET", url)

    def totals(self):
        """
        Gets transaction totals
        """
        url = self._url("/transaction/totals/")
        return self._handle_request("GET", url)

    def initialize(
        self, email, amount, plan=None, reference=None, channel=None, metadata=None
    ):
        """
        Initialize a transaction and returns the response

        args:
        email -- Customer's email address
        amount -- Amount to charge
        plan -- optional
        Reference -- optional
        channel -- channel type to use
        metadata -- a list if json data objects/dicts
        """
        amount = utils.validate_amount(amount)

        if not email:
            raise InvalidDataError("Customer's Email is required for initialization")

        url = self._url("/transaction/initialize")
        payload = {
            "email": email,
            "amount": amount,
        }

        if plan:
            payload.update({"plan": plan})
        if channel:
            payload.update({"channels": channel})
        if reference:
            payload.update({"reference": reference})
        if metadata:
            payload.update({"metadata": metadata})

        return self._handle_request("POST", url, payload)

    def charge(self, email, auth_code, amount, reference=None, metadata=None):
        """
        Charges a customer and returns the response

        args:
        auth_code -- Customer's auth code
        email -- Customer's email address
        amount -- Amount to charge
        reference -- optional
        metadata -- a list if json data objects/dicts
        """
        amount = utils.validate_amount(amount)

        if not email:
            raise InvalidDataError("Customer's Email is required to charge")

        if not auth_code:
            raise InvalidDataError("Customer's Auth code is required to charge")

        url = self._url("/transaction/charge_authorization")
        payload = {
            "authorization_code": auth_code,
            "email": email,
            "amount": amount,
        }

        if reference:
            payload.update({"reference": reference})
        if metadata:
            payload.update({"metadata": {"custom_fields": metadata}})

        return self._handle_request("POST", url, payload)

    def verify(self, reference):
        """
        Verifies a transaction using the provided reference number

        args:
        reference -- reference of the transaction to verify
        """

        reference = str(reference)
        url = self._url("/transaction/verify/{}".format(reference))
        return self._handle_request("GET", url)

    def fetch_transfer_banks(self):
        """
        Fetch transfer banks
        """

        url = self._url("/bank")
        return self._handle_request("GET", url)

    def create_transfer_customer(self, bank_code, account_number, account_name):
        """
        Create a transfer customer
        """
        url = self._url("/transferrecipient")
        payload = {
            "type": "nuban",
            "currency": "NGN",
            "bank_code": bank_code,
            "account_number": account_number,
            "name": account_name,
        }
        return self._handle_request("POST", url, payload)

    def transfer(self, recipient_code, amount, reason, reference=None):
        """
        Initiates transfer to a customer
        """
        amount = utils.validate_amount(amount)
        url = self._url("/transfer")
        payload = {
            "amount": amount,
            "reason": reason,
            "recipient": recipient_code,
            "source": "balance",
            "currency": "NGN",
        }
        if reference:
            payload.update({"reference": reference})

        return self._handle_request("POST", url, payload)
