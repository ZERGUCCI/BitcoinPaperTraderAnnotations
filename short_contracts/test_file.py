import sys
import unittest
from trading_system import Wallet
import numpy as np

class TestShort(unittest.TestCase):
    
    def setUp(self):
        self.wallet = Wallet(10000)

    def test_short(self):
        self.wallet.short(1, 1000, 1)

        self.assertEqual(self.wallet.cash, 11000)
        self.assertEqual(self.wallet.short_stock, 1)
    
    def test_close_short(self):
        self.wallet.short(1, 1000, 1)

        self.assertEqual(self.wallet.cash, 11000)
        self.assertEqual(self.wallet.short_stock, 1)

        self.wallet.close_short(2, 900, 1)
        self.assertEqual(self.wallet.cash, 10100)
        self.assertEqual(self.wallet.short_stock, 0)
    
    def short_input_validation(self):

        # Short more than can buy
        self.assertFalse(self.wallet.short(1, 1000, 11))
        
        # Short back in time
        self.wallet.buy(1, 1000, 1)
        self.assertFalse(self.wallet.short(0, 1000, 1))

        # Short negative price
        self.assertFalse(self.wallet.short(2, -1, 100))

        # Short negative number
        self.assertFalse(self.wallet.short(3, 1000, -1))
    
    def test_close_short_input_validation(self):

        self.wallet.short(1, 1000, 10)

        # Trying to close more than currently short
        self.assertFalse(self.wallet.close_short(1, 1000, 11))
        
        # Trying to close back in time
        self.assertFalse(self.wallet.close_short(0, 1000, 1))

        # Closing with negative price
        self.assertFalse(self.wallet.close_short(2, -1, 1))

        # Closing negative number
        self.assertFalse(self.wallet.close_short(3, 1000, -1))

        # Closing without shorting any
        new_wallet = Wallet(10000)
        self.assertFalse(new_wallet.close_short(1, 1000, 1))


def main():
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestShort))
    runner = unittest.TextTestRunner()

    if runner.run(suite).wasSuccessful():
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()