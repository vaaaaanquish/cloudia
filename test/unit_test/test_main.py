from cloudia.main import Cloudia
import unittest


class TestCloudia(unittest.TestCase):
    def setUp(self):
        self.cls = Cloudia('test')

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
