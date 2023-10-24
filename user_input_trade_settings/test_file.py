import sys
import unittest
import pytz

from trading_system import load_historical_data, user_settings
from datetime import datetime

class TestUserSettings(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Load data once before running all test cases
        cls.historical_data = load_historical_data('HistoricalBTCdata.txt')
    
    #test input validation for wallet
    def test_invalid_wallet(self):
        wallet, adjusted_data = user_settings(-1000, '01-02-2017', '01-03-2017', 60, self.historical_data)
        self.assertIsNone(wallet)
        self.assertIsNone(adjusted_data, "Negative wallet value accepted")

    # Test input validation for dates
    def test_invalid_date(self):
        wallet, adjusted_data = user_settings(1000, '12-03-2017', '01-01-2017', 60, self.historical_data)
        self.assertIsNone(wallet)
        self.assertIsNone(adjusted_data, "Invalid date range accepted")

    # Test input validation for time interval
    def test_invalid_time_interval(self):
        wallet, adjusted_data = user_settings(1000, '01-02-2017', '01-03-2017', 59, self.historical_data)
        self.assertIsNone(wallet)
        self.assertIsNone(adjusted_data, "Invalid time interval accepted")

    # Test that adjusted data is between start and end input dates
    def test_data_filtering(self):
        wallet, adjusted_data = user_settings(1000, '01-02-2017', '01-03-2017', 60, self.historical_data)

        utc_tz = pytz.utc
        start_date_obj = datetime.strptime('01-02-2017', '%m-%d-%Y')
        end_date_obj = datetime.strptime('01-03-2017', '%m-%d-%Y')
        start_date_obj = utc_tz.localize(start_date_obj)
        end_date_obj = utc_tz.localize(end_date_obj)
        start_timestamp = int(start_date_obj.timestamp()) + 60
        end_timestamp = int(end_date_obj.timestamp()) + 60

        self.assertTrue(all(start_timestamp <= data_point[0] <= end_timestamp for data_point in adjusted_data), "Incorrect data filtering")

    # Check data is corrrectly adjusted according to time interval
    def test_data_adjustment(self):
        wallet, adjusted_data = user_settings(1000, '01-02-2017', '01-03-2017', 120, self.historical_data)
        times = [data_point[0] for data_point in adjusted_data]
        self.assertTrue(all((times[i + 1] - times[i]) == 120 for i in range(len(times) - 1)), "Incorrect data adjustment")

    # Test decimal wallet inputs
    def test_valid_wallet_wallet(self):
        wallet, adjusted_data = user_settings(1000.5, '01-02-2017', '01-03-2017', 60, self.historical_data)
        self.assertEqual(wallet, 1000.5, "Wallet not properly initialized")

    # Test function correctly accepts valid dates
    def test_valid_date(self):
        wallet, adjusted_data = user_settings(1000, '01-02-2017', '01-03-2017', 60, self.historical_data)
        self.assertEqual(wallet, 1000)

def main():
    suite = unittest.TestSuite()

    test_cases = unittest.TestLoader().loadTestsFromTestCase(TestUserSettings)
    suite.addTests(test_cases)

    result = unittest.TextTestRunner().run(suite)

    if result.wasSuccessful():
        sys.exit(0)  # All tests passed, exit with code 0
    else:
        sys.exit(1)  # Some tests failed, exit with code 1

if __name__ == "__main__":
    main()