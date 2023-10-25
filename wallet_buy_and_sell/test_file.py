import sys
import unittest
from trading_system import Wallet
import numpy as np

class TestWallet(unittest.TestCase):
    
    def setUp(self):
        self.wallet = Wallet(10000)

    def test_initial_wallet_state(self):
        self.assertEqual(self.wallet.cash, 10000)
        self.assertEqual(self.wallet.stock, 0)
        self.assertEqual(self.wallet.transactions, [])

    def test_buy_operation(self):
        self.assertEqual(self.wallet.cash, 10000)
        self.assertTrue(self.wallet.buy(1001, 10, 1))
        self.assertEqual(self.wallet.cash, 9990)
        self.assertEqual(self.wallet.stock, 1)
        # Test Logging
        self.assertEqual(self.wallet.transactions[-1], {
            'type': 'buy', 'price': 10, 'number': 1, 'timestamp': 1001})

    def test_sell_operation(self):
        self.assertTrue(self.wallet.buy(1000, 100, 1))
        self.assertTrue(self.wallet.sell(1100, 200, 0.5))
        self.assertEqual(self.wallet.cash, 10000)
        self.assertEqual(self.wallet.stock, 0.5)
        # Test Logging
        self.assertEqual(self.wallet.transactions[-1], {
            'type': 'sell', 'price': 200, 'number': 0.5, 'timestamp': 1100})

    def test_buy_invalid_timestamp(self):
        self.assertTrue(self.wallet.buy(1000, 100, 1))
        self.assertFalse(self.wallet.buy(900, 50, 0.5))  # Cannot buy before previous transaction.

    def test_sell_invalid_timestamp(self):
        self.assertTrue(self.wallet.buy(1000, 100, 1))
        self.assertFalse(self.wallet.sell(900, 150, 0.5))  # Cannot sell before previous transaction.

    def test_invalid_price(self):
        self.assertFalse(self.wallet.buy(1200, np.nan, 0.5))  # Invalid price
        self.assertFalse(self.wallet.buy(1200, -10, 0.5))  

    def test_not_enough_cash(self):
        self.assertFalse(self.wallet.buy(1200, 20000, 1))  # Not enough cash to buy that number

    def test_invalid_number(self):
        self.assertFalse(self.wallet.buy(1200, 10, -1))  # Cannot buy 0 or negative amount
    
    def test_multiple_buys(self):
        self.assertTrue(self.wallet.buy(1000, 5000, 1))
        self.assertTrue(self.wallet.buy(1100, 4000, 1))
        self.assertEqual(self.wallet.stock, 2)
        self.assertEqual(self.wallet.cash, 1000)
        self.assertFalse(self.wallet.buy(1200, 3000, 1)) # Cannot buy more than amount of cash left

    def test_multiple_sells(self):
        self.assertTrue(self.wallet.buy(1000, 5000, 1))
        self.assertTrue(self.wallet.sell(1100, 10000, 0.5))
        self.assertTrue(self.wallet.sell(1200, 20000, 0.5))
        self.assertEqual(self.wallet.stock, 0)
        self.assertEqual(self.wallet.cash, 20000)
        self.assertFalse(self.wallet.sell(1300, 30000, 0.1)) # Cannot sell more than stock number in wallet

def main():
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestWallet))
    runner = unittest.TextTestRunner()

    if runner.run(suite).wasSuccessful():
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()