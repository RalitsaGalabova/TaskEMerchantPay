API_Test.py is an console application and tests the basic functionality of a simple payment application that allows you to trigger Sale and Void transactions and receive the transaction's status and unique identifier.

The application consists of two methods that generate user credentials from a configuration file "configuration_file.config" 
and five tests that evaluate the main functionality:
-test_valid_payment_transaction tests if it is possible to create a valid transaction
-test_valid_void_transaction tests if it is possible to void valid transaction
-test_valid_payment_transaction_with_invalid_authentication verifies that it is not possible to create a transaction with invalid credentials
-test_valid_void_transaction_pointing_to_nonexistent_payment_transaction verifies that it is not possible to void transaction that does not exist
-test_valid_void_transaction_pointing_to_existent_payment_transaction tests if it is possible to void a transaction that is already voided
