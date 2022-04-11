"""Sorts."""
from operator import attrgetter, itemgetter


def sort_multi_ordering(data, ordering, mode="dict"):
    """다중 정렬하기.

    References:
        https://docs.python.org/ko/3/howto/sorting.html#sort-stability-and-complex-sorts
    """
    specs = []
    for order in ordering:
        if isinstance(order, str):
            reverse = order.startswith("-")
            specs.append((order[reverse:], reverse))
        else:
            specs.append(order)

    for key, reverse in reversed(specs):
        if mode == "dict":
            data.sort(key=lambda x: x[key], reverse=reverse)
        elif mode == "item":
            data.sort(key=itemgetter(key), reverse=reverse)
        else:
            data.sort(key=attrgetter(key), reverse=reverse)
    return data
