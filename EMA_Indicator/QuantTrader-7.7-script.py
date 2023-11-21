import sys
import unittest

class TestEMA(unittest.TestCase):

    def setUp(self):
        self.data_points = [{'close': price} for price in [1, 2, 3, 4, 5]]

    def test_exponential_moving_average(self):
        from trading_system import TechnicalIndicators

        # Manual EMA calculation based on dataset
        expected_ema = (5 * (2/(3+1))) +  (3 * (1 - (2/(3+1))))

        ema = TechnicalIndicators.exponential_moving_average(self.data_points, 3)

        self.assertAlmostEqual(ema, expected_ema, places=6)

    def test_exponential_moving_average_with_different_data(self):
        from trading_system import TechnicalIndicators

        different_data_points = [{'close': price} for price in [11, 21, 31, 41, 51]]

        # Manual EMA calculation based on provided dataset
        expected_ema = (2/(3+1)) * 51 + (1 - (2/(3+1))) * 31

        ema = TechnicalIndicators.exponential_moving_average(different_data_points, 3)

        self.assertAlmostEqual(ema, expected_ema, places=6)
        
    def test_exponential_moving_average_raise_value_error(self):
        from trading_system import TechnicalIndicators

        short_data_points = [{'close': price} for price in [1, 2]]

        # The function should raise a ValueError if the data is too short
        self.assertRaises(ValueError, TechnicalIndicators.exponential_moving_average, short_data_points, 3)

def main():
    # helper.install_requirements("test_scripts/QuantTrader_requirements.txt")
    
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestEMA))
    runner = unittest.TextTestRunner()

    if runner.run(suite).wasSuccessful():
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    # helper = CoderEvalHelper()
    main()