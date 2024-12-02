import unittest

from sprites import Gem


class GemTest(unittest.TestCase):

    def setUp(self):
        self.gem = Gem(200, 200)

    def test_gem_default_value(self):
        self.assertEqual(100, self.gem._value)

    def test_gem_value_initializes_with_alternate_value(self):
        gem = Gem(value=300)
        self.assertEqual(300, gem.value)

    def test_gem_can_be_moved(self):
        self.gem.place(400, 420)
        self.assertEqual(400, self.gem.rect.x)
        self.assertEqual(420, self.gem.rect.y)
