import sys
import unittest
from trading_system import Wallet

class TestSummary(unittest.TestCase):
    
    def setUp(self):
        self.wallet = Wallet(50)
    
    def test_total_profits(self):
        final_wallet = 100

        expected_net = 50
        expected_percentage = 100.0

        net, percentage = self.wallet.totalProfits(50,final_wallet)
        self.assertEqual(expected_net, net)
        self.assertEqual(expected_percentage, percentage)


    def test_percent_profitable(self):
        transactions = [
            {'type': 'buy', 'price': 10, 'number': 5, 'timestamp': 1},
            {'type': 'sell', 'price': 15, 'number': 5, 'timestamp': 2},
            {'type': 'buy', 'price': 20, 'number': 2, 'timestamp': 3},
            {'type': 'sell', 'price': 10, 'number': 2, 'timestamp': 4},
            {'type': 'short', 'price': 10, 'number': 5, 'timestamp': 5},
            {'type': 'close_short', 'price': 5, 'number': 5, 'timestamp': 6},
            {'type': 'short', 'price': 10, 'number': 2, 'timestamp': 7},
            {'type': 'close_short', 'price': 15, 'number': 2, 'timestamp': 8},
        ]

        self.wallet.transactions = transactions
        expected_percent_profitable = 50.0 
        self.assertEqual(self.wallet.percentProfitable(), expected_percent_profitable)
    
    def test_total_closed_trades(self):
        transactions = [
            {'type': 'buy', 'price': 10, 'number': 5, 'timestamp': 1},
            {'type': 'sell', 'price': 15, 'number': 5, 'timestamp': 2},
            {'type': 'buy', 'price': 20, 'number': 2, 'timestamp': 3},
            {'type': 'sell', 'price': 10, 'number': 2, 'timestamp': 4},
            {'type': 'short', 'price': 10, 'number': 5, 'timestamp': 5},
            {'type': 'close_short', 'price': 5, 'number': 5, 'timestamp': 6},
            {'type': 'short', 'price': 10, 'number': 2, 'timestamp': 7},
            {'type': 'close_short', 'price': 15, 'number': 2, 'timestamp': 8},
        ]
        self.wallet.transactions = transactions
        expected_total = 4
        self.assertEqual(self.wallet.totalClosedTrades(), expected_total)

    def test_profit_factor(self):
        transactions = [
            {'type': 'buy', 'price': 10, 'number': 5, 'timestamp': 1},
            {'type': 'sell', 'price': 15, 'number': 5, 'timestamp': 2}, # profit = 25
            {'type': 'buy', 'price': 20, 'number': 2, 'timestamp': 3},
            {'type': 'sell', 'price': 10, 'number': 2, 'timestamp': 4}, # profit = -20
            {'type': 'short', 'price': 10, 'number': 5, 'timestamp': 5},
            {'type': 'close_short', 'price': 5, 'number': 5, 'timestamp': 6}, # profit = 25
            {'type': 'short', 'price': 10, 'number': 2, 'timestamp': 7},
            {'type': 'close_short', 'price': 15, 'number': 2, 'timestamp': 8}, # profit = -10
        ]
        self.wallet.transactions = transactions

        expected_profit_factor = 1.6666666666666 # 50/30
        self.assertAlmostEqual(self.wallet.profitFactor(), expected_profit_factor)



def main():
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestSummary))
    runner = unittest.TextTestRunner()

    if runner.run(suite).wasSuccessful():
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
