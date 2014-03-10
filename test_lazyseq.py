import unittest

from lazyseq import LazySeq


class Cases(object):
    def test_items(self):
        self.assertEqual(list(self.seq), list(range(5)))

    def test_cache(self):
        self.assertEqual(self.seq._cached_items, [])
        self.seq.cache(0)
        self.assertEqual(self.seq._cached_items, [])
        self.seq.cache(1)
        self.assertEqual(self.seq._cached_items, [0])
        self.seq.cache(3)
        self.assertEqual(self.seq._cached_items, [0, 1, 2])
        self.seq.cache()
        self.assertEqual(self.seq._cached_items, list(range(5)))

    def test_getitem_simple(self):
        self.assertEqual(self.seq[0], 0)
        self.assertEqual(self.seq._cached_items, [0])
        self.assertEqual(self.seq[:3], [0, 1, 2])
        self.assertEqual(self.seq._cached_items, [0, 1, 2])
        self.assertEqual(self.seq[:], list(range(5)))
        self.assertEqual(self.seq._cached_items, list(range(5)))

    def test_getitem_complex(self):
        self.assertEqual(self.seq[1:3], [1, 2])
        self.assertEqual(self.seq._cached_items, list(range(3)))

    def test_getitem_complex2(self):
        self.assertEqual(self.seq[3:1:-1], [3, 2])
        self.assertEqual(self.seq._cached_items, list(range(4)))

    def test_getitem_negative(self):
        self.assertEqual(self.seq[-1], 4)
        self.assertEqual(self.seq._cached_items, list(range(5)))

    def test_repr(self):
        self.assertEqual(repr(self.seq), 'LazySeq([...])')
        self.seq.cache(1)
        self.assertEqual(repr(self.seq), 'LazySeq([0, ...])')
        self.seq.cache(3)
        self.assertEqual(repr(self.seq), 'LazySeq([0, 1, 2, ...])')
        self.seq.cache()
        self.assertEqual(repr(self.seq), 'LazySeq([0, 1, 2, 3, 4])')


class TestListLazySeq(unittest.TestCase, Cases):
    def setUp(self):
        self.seq = LazySeq(list(range(5)))


class TestRangeLazySeq(unittest.TestCase, Cases):
    def setUp(self):
        self.seq = LazySeq(range(5))


class TestGeneratorLazySeq(unittest.TestCase, Cases):
    def setUp(self):
        self.seq = LazySeq(i for i in range(5))
