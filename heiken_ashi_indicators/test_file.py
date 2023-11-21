import sys
import unittest

from trading_system import minute_to_ohlc, TechnicalIndicators

class TestTechnicalIndicators(unittest.TestCase):

    def setUp(self):
        # Timestamps are spaced 60 seconds apart
        self.data_points = [[i * 60, i] for i in range(1, 11)]
        
    def test_minute_to_ohlc(self):
        ohlc_data = minute_to_ohlc(self.data_points, 5)

        expected_ohlc_data = [
            {'timestamp': 60, 'open': 1, 'high': 5, 'low': 1, 'close': 5},
            {'timestamp': 360, 'open': 6, 'high': 10, 'low': 6, 'close': 10}
        ]
        
        self.assertEqual(ohlc_data, expected_ohlc_data)

    def test_heikin_ashi(self):
        ohlc_data = minute_to_ohlc(self.data_points, 5)

        prev_candle = None
        for data_point in ohlc_data:
            new_candle = TechnicalIndicators.heikin_ashi(data_point, prev_candle)
            prev_candle = new_candle

        # Manual Heiken Ashi Calculation based on dataset
        expected_new_candle = { 'open': 3, 'close': 8, 'high': 10, 'low': 3 }
        
        self.assertEqual(new_candle, expected_new_candle)

def main():
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestTechnicalIndicators))
    runner = unittest.TextTestRunner()

    if runner.run(suite).wasSuccessful():
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()