import unittest, utils

class TestUtils(unittest.TestCase):

    def test_pos_to_cell_ref(self):
        pos = [1, 1]
        expected_result = "A1"
        self.assertEqual(utils.pos_to_cell_ref(pos), expected_result)

if __name__ == "__main__":
    unittest.main()
