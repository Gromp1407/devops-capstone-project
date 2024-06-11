import unittest
from your_application import create_app, db
from your_application.models import Account
from flask_api import status

class TestAccountService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """ Set up the test environment """
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.app.config['DEBUG'] = False
        cls.client = cls.app.test_client()
        with cls.app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        """ Tear down the test environment """
        with cls.app.app_context():
            db.session.remove()
            db.drop_all()

    def _create_accounts(self, count):
        """ Helper function to create accounts in bulk """
        accounts = []
        for _ in range(count):
            account = Account(name="test_account", email="test@example.com", address="123 test st")
            db.session.add(account)
            db.session.commit()
            accounts.append(account)
        return accounts

    def test_get_account(self):
        """It should Read a single Account"""
        # Create an account using a POST request
        account_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "address": "1234 Main St"
        }
        create_resp = self.client.post(
            "/accounts",
            json=account_data,
            content_type="application/json"
        )
        self.assertEqual(create_resp.status_code, status.HTTP_201_CREATED)
        created_account = create_resp.get_json()

        # Read the account using a GET request
        get_resp = self.client.get(
            f"/accounts/{created_account['id']}",
            content_type="application/json"
        )
        self.assertEqual(get_resp.status_code, status.HTTP_200_OK)
        data = get_resp.get_json()
        self.assertEqual(data["name"], account_data["name"])
        self.assertEqual(data["email"], account_data["email"])
        self.assertEqual(data["address"], account_data["address"])

if __name__ == "__main__":
    unittest.main()
