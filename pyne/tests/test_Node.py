import unittest

from pyne.decision import Decision



class TestNode(unittest.TestCase):

    def test_Name(self):
        n = Decision("Coucou")
        self.assertEqual("Decision: Coucou", str(n))



if __name__ == '__main__':
    unittest.main()
