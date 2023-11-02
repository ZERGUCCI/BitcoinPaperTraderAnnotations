import sys
import unittest
from trading_system import Wallet, SimpleMovingAverageStrategy
import numpy as np
from unittest.mock import MagicMock

class TestSMA(unittest.TestCase):
    
    def setUp(self):
        self.wallet = Wallet(1000)
        self.data_points = [{'timestamp': 1, 'close': 2},
                            {'timestamp': 2, 'close': 3},
                            {'timestamp': 3, 'close': 1},
                            {'timestamp': 4, 'close': 5}]
        self.sma_strategy = SimpleMovingAverageStrategy(self.wallet, self.data_points, 2)

    def test_wallet_ending_cash_and_shares(self):
        self.sma_strategy.execute()

        self.assertEqual(self.wallet.cash, 5000)
        self.assertEqual(self.wallet.stock, 0)
        self.assertEqual(self.wallet.short_stock, 0)




def main():
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestSMA))
    runner = unittest.TextTestRunner()

    if runner.run(suite).wasSuccessful():
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()