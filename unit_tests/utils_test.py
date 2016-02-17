import unittest, utils


class TestUtils(unittest.TestCase):

    CELL_REF_TO_EXPECTED_POS_EXAMPLES = {
        "A1": [1, 1],
        "B1": [1, 2],
        "H1": [1, 8],
        "A2": [2, 1],
        "H2": [2, 8],
        "A8": [8, 1],
        "B8": [8, 2],
        "H8": [8, 8]}


    def test_cell_ref_to_pos(self):
        """
        Test to ensure that cell references are converted to appropriate position lists.
        """
        for cell_ref, expected_pos in TestUtils.CELL_REF_TO_EXPECTED_POS_EXAMPLES.items():
            self.assertEqual(utils.cell_ref_to_pos(cell_ref), expected_pos)


    def test_pos_to_cell_ref(self):
        """
        Test to ensure that position lists are converted to appropriate cell references.
        """
        # invert dict and use tuples rather than lists for key as lists are not hashable
        test_input_pos_to_expected_cell_ref = {
            tuple(v): k for k, v in TestUtils.CELL_REF_TO_EXPECTED_POS_EXAMPLES.items()}

        for pos, expected_cell_ref in test_input_pos_to_expected_cell_ref.items():
            self.assertEqual(utils.pos_to_cell_ref(list(pos)), expected_cell_ref)


if __name__ == "__main__":
    unittest.main()
