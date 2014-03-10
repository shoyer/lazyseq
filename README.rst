lazyseq: a lazily evaluated sequence type for Python
----------------------------------------------------

|travis|

**lazyseq** is a simple library implementing a single class, ``LazySeq``, which
provides a lazily evaluated sequence that can be used like an immutable list.
You can think of it as a Pythonic version of Clojure's
`Seq <http://clojure.org/sequences>`_.

``LazySeq`` implements Python’s sequence interface, and thus has the methods
``__getitem__``, ``__len__``, ``__contains__``, ``__iter__``, ``__reversed__``,
``index``, and ``count``.

Getting an item from a LazySeq is equivalent to getting an items from the
provided iterable as a list. However, only the necessary elements of the
iterable are evaluated (all those up to the maximum requested element), and all
evaluated elements are cached on the ``LazySeq`` so it can be iterated over
again. Note that some operations like ``len(seq)`` will by necessity iterate
over (and thus cache) the entire iterable.

To use LazySeq, just wrap any Python iterable (including a generator
comprehensions, of course) in LazySeq:

.. code:: python

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

.. |travis| image:: https://travis-ci.org/shoyer/lazyseq.png
    :target: https://travis-ci.org/shoyer/lazyseq
    :alt: travis-ci build status
