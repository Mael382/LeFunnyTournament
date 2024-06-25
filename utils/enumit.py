from collections.abc import Iterable, Sequence, Iterator


def reversed_enumerate(collection: Sequence) -> Iterator[int, ...]:
    """
    ...

    :param collection:
    :return:
    """
    for index in range(len(collection) - 1, -1, -1):
        yield index, collection[index]


def sorted_iterate(collection: Iterable, *, key=None, reverse=False) -> Iterator:
    """
    ...

    :param collection:
    :param key:
    :param reverse:
    :return:
    """
    for item in sorted(collection, key=key, reverse=reverse):
        yield item
