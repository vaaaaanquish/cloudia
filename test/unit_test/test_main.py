from cloudia.main import CloudiaBase
import unittest


class TestCloudia(unittest.TestCase):
    # TODO: split test case
    def setUp(self):
        self.cls = CloudiaBase('test')

    def test_calc_fig_size(self):
        # row_num==item_num==1
        output = self.cls._calc_fig_size(1, 1, 1)
        self.assertTupleEqual(output, (10, 6))

        # rate
        output = self.cls._calc_fig_size(1, 1, 2)
        self.assertTupleEqual(output, (20, 12))

        # item_num<=row_num
        output = self.cls._calc_fig_size(1, 2, 1)
        self.assertTupleEqual(output, (5, 9))

        output = self.cls._calc_fig_size(1, 2, 2)
        self.assertTupleEqual(output, (10, 18))

        # item_num // row_num + 1 < row_num
        output = self.cls._calc_fig_size(2, 3, 1)
        self.assertTupleEqual(output, (10, 6))

        output = self.cls._calc_fig_size(2, 3, 2)
        self.assertTupleEqual(output, (20, 12))

        # else
        output = self.cls._calc_fig_size(3, 10, 1)
        self.assertTupleEqual(output, (15, 12))

        output = self.cls._calc_fig_size(3, 10, 2)
        self.assertTupleEqual(output, (30, 24))

    def test_calc_wc_size(self):
        output = self.cls._calc_wc_size(1)
        self.assertTupleEqual(output, (500, 300))

        output = self.cls._calc_wc_size(2)
        self.assertTupleEqual(output, (1000, 600))

    def test_calc_sub_plot_dimensions(self):
        output = self.cls._calc_sub_plot_dimensions(10, 3)
        self.assertTupleEqual(output, (4, 3))

        output = self.cls._calc_sub_plot_dimensions(1, 3)
        self.assertTupleEqual(output, (1, 1))

        output = self.cls._calc_sub_plot_dimensions(2, 2)
        self.assertTupleEqual(output, (2, 2))

    def test_color(self):
        output = self.cls._color(True, True)
        self.assertEqual(output, 'white')

        output = self.cls._color(True, False)
        self.assertEqual(output, 'black')

        output = self.cls._color(False, True)
        self.assertEqual(output, 'black')

        output = self.cls._color(False, False)
        self.assertEqual(output, 'white')
