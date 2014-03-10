from collections import Sequence
from itertools import islice


__version__ = '0.1.1'


class LazySeq(Sequence):
    """A lazily evaluated sequence that can be used like an immutable list

    LazySeq implements Python's sequence interface, and thus has the methods
    __getitem__, __len__, __contains__, __iter__, __reversed__, index, and
    count.

    Getting an item from a LazySeq is equivalent to getting an items from the
    provided iterable as a list. However, only the necessary elements of the
    iterable are evaluated (all those up to the maximum requested element), and
    all evaluated elements are cached on the LazySeq so it can be iterated over
    again. Note that some operations like `len(seq)` will by necessity iterate
    over (and thus cache) the entire iterable.

    To use LazySeq, just wrap any Python iterable (including generator
    comprehensions, of course) in LazySeq:

    >>> from lazyseq import LazySeq
    >>> seq = LazySeq(x ** 2 for x in range(5))
    >>> seq
    LazySeq([...])
    >>> seq[:3]
    [0, 1, 4]
    >>> seq
    LazySeq([0, 1, 4, ...])
    >>> list(seq)
    [0, 1, 4, 9, 16]
    >>> seq
    LazySeq([0, 1, 4, 9, 16])
    """
    def __init__(self, iterable):
        self._iterator = iter(iterable)
        self._exhausted = False
        self._cached_items = []

    def __getitem__(self, key):
        if isinstance(key, int) and key >= 0:
            self.cache(key + 1)
        elif (isinstance(key, slice) and key.stop is not None and key.stop >= 0
              and (key.start is None or key.start >= 0)):
            start = 0 if key.start is None else key.start
            self.cache(max(start + 1, key.stop))
        else:
            self.cache()
        return self._cached_items[key]

    def _iter_uncached(self):
        for item in self._iterator:
            self._cached_items.append(item)
            yield item
        self._exhausted = True

    def __iter__(self):
        for item in self._cached_items:
            yield item
        for item in self._iter_uncached():
            yield item

    def cache(self, n=None):
        """Insure that all items up through the nth element in the sequence (or
        all items, if n is None) are cached internally
        """
        if n is None:
            items = self._iter_uncached()
        elif n > len(self._cached_items):
            items = islice(self._iter_uncached(), n - len(self._cached_items))
        else:
            items = []

        for item in items:
            pass

    def __len__(self):
        self.cache()
        return len(self._cached_items)

    def __repr__(self):
        items_str = ', '.join(repr(i) for i in self._cached_items)
        if self._cached_items and not self._exhausted:
            items_str += ', '
        if not self._exhausted:
            items_str += '...'
        return '%s([%s])' % (type(self).__name__, items_str)
