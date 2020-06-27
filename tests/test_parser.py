import unittest
import medparse


class ParseTestCase(unittest.TestCase):
    def setUp(self):
        self.medp = medparse.MedParse('47', '2', 'парацетамол')

    def test_get_region(self):
        return self.assertRaises('AttributeError', self.medp.area)


if __name__ == '__main__':
    unittest.main()

