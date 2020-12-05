from . import test_auth_key, Customer, TestCase


class TestCustomerRecords(TestCase):
    def setUp(self):
        super(TestCustomerRecords, self).setUp()
        self.assertNotEqual(test_auth_key, None)
        self.customer = Customer(authorization_key=test_auth_key)

    def test_customers_records(self):
        """
        Integration test for getting all customers and getting single customer details
        """
        def retrieve_all_customers():
            (status_code, status, response_msg,
             customers_list) = self.customer.getall()
            self.assertEqual(status_code, 200)
            self.assertEqual(status, True)
            self.assertEqual(response_msg, 'Customers retrieved')
            self.assertIsInstance(customers_list, list)
            return customers_list

        def retrieve_one_customer():
            one_customer = customers_list[0]
            (status_code, status, response_msg,
             customer_data) = self.customer.getone(one_customer['customer_code'])
            self.assertEqual(status_code, 200)
            self.assertEqual(status, True)
            self.assertEqual(response_msg, 'Customer retrieved')
            # assert if subset
            self.assertLessEqual(one_customer.items(), customer_data.items())

        customers_list = retrieve_all_customers()
        retrieve_one_customer()
