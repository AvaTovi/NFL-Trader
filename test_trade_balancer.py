import unittest
from trade_balancer import find_best_trade

class SimpleTradeTest(unittest.TestCase):
    def test_simple_1_for_1_positive_gain(self):
        # small dummy rosters
        teamA = [
            {'name':'A','rating':90,'salary':30,'contract':1},
            {'name':'B','rating':80,'salary':20,'contract':1}
        ]
        teamB = [
            {'name':'X','rating':88,'salary':30,'contract':1},
            {'name':'Y','rating':78,'salary':20,'contract':1}
        ]

        # run 1-for-1
        result = find_best_trade(teamA, teamB, 1, 1)
        # result should not be None
        self.assertIsNotNone(result, "Expected a trade result, got None")

        give, get, details = result

        # rating_gain should be > 0 (we expect a slight upgrade)
        self.assertIn('rating_gain', details, "Missing rating_gain in details")
        self.assertGreater(details['rating_gain'], 0,
                           f"Expected positive rating_gain, got {details['rating_gain']}")

        # ensure exactly one player on each side
        self.assertEqual(len(give), 1)
        self.assertEqual(len(get), 1)

if __name__ == '__main__':
    unittest.main()
