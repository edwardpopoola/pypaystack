from . import test_auth_key, Transaction, TestCase


class TestTransaction(TestCase):
    def setUp(self):
        super(TestTransaction, self).setUp()
        self.assertNotEqual(test_auth_key, None)
        self.transaction = Transaction(authorization_key=test_auth_key)

    def test_charge_and_verify(self):
        """
        Integration test for initiating and verifying transactions
        """
        transaction_details = {
            "amount": 1000*100,
            "email": "test_customer@mail.com",
            "currency": "USD"
        }

        def initialize_transaction():
            (status_code, status, response_msg,
             initialized_transaction_data) = self.transaction.initialize(**transaction_details)
             
            self.assertEqual(status_code, 200)
            self.assertEqual(status, True)
            self.assertEqual(response_msg, 'Authorization URL created')
            return initialized_transaction_data

        def verify_transaction():
            (status_code, status, response_msg, response_data) = self.transaction.verify(
                reference=initialized_transaction_data['reference'])
            self.assertEqual(status_code, 200)
            self.assertEqual(status, True)
            self.assertEqual(response_msg, 'Verification successful')
            self.assertEqual(response_data.get('customer')
                             ['email'], transaction_details['email'])

        initialized_transaction_data = initialize_transaction()
        verify_transaction()
