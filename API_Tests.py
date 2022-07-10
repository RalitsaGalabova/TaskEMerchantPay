import unittest
import json
import requests
import base64
import configparser


transaction_id = ""

# Gets credentilas from config file
def get_creds():
    '''config_file = "creds.config"
    with open(config_file, 'rb') as f:
        data = f.read()
    token = base64.b64encode(data.strip())
    return token.decode()'''

    config = configparser.ConfigParser()
    config.read('configuration_file.config')
    arr = bytes(config['Credentials']['credentials'], 'utf-8')
    token = base64.b64encode(arr)

    return token.decode()


# Gets invalid credentilas from config file
def get_invalid_creds():

    config = configparser.ConfigParser()
    config.read('configuration_file.config')
    arr = bytes(config['Credentials']['credentials_invalid'], 'utf-8')
    token = base64.b64encode(arr)

    return token.decode()



class TestingAPI(unittest.TestCase):

    def test_valid_payment_transaction(self):
        # Arrange
        global transaction_id
        token = get_creds()
        headers = {"Content-Type": "application/json;charset=UTF-8", "Authorization": "Basic " + token}
        data = {
            "payment_transaction": {
                "card_number": "4200000000000000",
                "cvv": "123",
                "expiration_date": "06/2019",
                "amount": "500",
                "usage": "Coffeemaker",
                "transaction_type": "sale",
                "card_holder": "Panda Panda",
                "email": "panda@example.com",
                "address": "Panda Street, China"
            }
        }

        # Act
        req = requests.post('http://localhost:3001/payment_transactions', json=data, headers=headers)
        res = json.loads(req.text)

        # Assert
        self.assertEqual(res["status"], "approved")
        self.assertEqual(req.status_code, 200)

        transaction_id = res["unique_id"]

    def test_valid_void_transaction(self):
        # Arrange
        global transaction_id
        token = get_creds()
        headers = {"Content-Type": "application/json;charset=UTF-8", "Authorization": "Basic " + token}
        data_void = {
            "payment_transaction": {
                "reference_id": transaction_id,
                "transaction_type": "void"}
        }

        # Act
        req = requests.post('http://localhost:3001/payment_transactions', json=data_void, headers=headers)
        res = json.loads(req.text)

        # Assert
        self.assertEqual(res["status"], "approved")
        self.assertEqual(req.status_code, 200)

    def test_valid_payment_transaction_with_invalid_authentication(self):
        # Arrange
        token = get_invalid_creds()
        headers = {"Content-Type": "application/json;charset=UTF-8", "Authorization": "Basic " + token}
        data = {
            "payment_transaction": {
                "card_number": "4200000000000000",
                "cvv": "123",
                "expiration_date": "06/2019",
                "amount": "500",
                "usage": "Coffeemaker",
                "transaction_type": "sale",
                "card_holder": "Panda Panda",
                "email": "panda@example.com",
                "address": "Panda Street, China"
            }
        }

        # Act
        req = requests.post('http://localhost:3001/payment_transactions', json=data, headers=headers)

        # Assert
        self.assertEqual(req.status_code, 401)


    def test_valid_void_transaction_pointing_to_nonexistent_payment_transaction(self):
        # Arrange

        token = get_creds()
        headers = {"Content-Type": "application/json;charset=UTF-8", "Authorization": "Basic " + token}
        data_void = {
            "payment_transaction": {
                #Use randum invalid referance_id
                "reference_id": "656556565656555",
                "transaction_type": "void"}
        }

        # Act
        req = requests.post('http://localhost:3001/payment_transactions', json=data_void, headers=headers)
        res = json.loads(req.text)

        # Assert
        self.assertEqual(res["reference_id"], ['Invalid reference transaction!'])
        self.assertEqual(req.status_code, 422)

    def test_valid_void_transaction_pointing_to_existent_payment_transaction(self):
        # Arrange
        global transaction_id
        token = get_creds()
        headers = {"Content-Type": "application/json;charset=UTF-8", "Authorization": "Basic " + token}
        data_void = {
            "payment_transaction": {
                "reference_id": transaction_id,
                "transaction_type": "void"}
        }

        # Act
        req = requests.post('http://localhost:3001/payment_transactions', json=data_void, headers=headers)

        # Assert
        self.assertEqual(req.status_code, 422)


if __name__ == '__main__':
    unittest.main()
