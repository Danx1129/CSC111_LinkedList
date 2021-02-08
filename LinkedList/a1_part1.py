from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Optional

from a1_linked_list import LinkedList, _Node


################################################################################
# Question 0 (NOT FOR MARKS)
# Original LinkedList:
# _first -> 10 -> 20 -> 30 -> 40 -> 50 -> 60 -> None
# Perform searches for 50, 10 and 40, in this order

# Heuristic 1 (move to front)
# _first -> 50 -> 10 -> 20 -> 30 -> 40 -> 60 -> None
# _first -> 10 -> 50 -> 20 -> 30 -> 40 -> 60 -> None
# _first -> 40 -> 10 -> 50 -> 20 -> 30 -> 60 -> None

# Heuristic 2 (swap)
# _first -> 10 -> 20 -> 30 -> 50 -> 40 -> 60 -> None
# _first -> 10 -> 20 -> 30 -> 50 -> 40 -> 60 -> None
# _first -> 10 -> 20 -> 30 -> 40 -> 50 -> 60 -> None

# Heuristic 3 (count)
# Original count LinkedList:
# _first -> 10 (0) -> 20 (0) -> 30 (0) -> 40 (0) -> 50 (0) -> 60 (0) -> None

# _first -> 50 (1) -> 10 (0) -> 20 (0) -> 30 (0) -> 40 (0) -> 60 (0) -> None
# _first -> 10 (1) -> 50 (1) -> 20 (0) -> 30 (0) -> 40 (0) -> 60 (0) -> None
# _first -> 10 (1) -> 40 (1) -> 50 (1) -> 20 (0) -> 30 (0) -> 60 (0) -> None
################################################################################

################################################################################
# Heuristic 1 (move to front)
################################################################################
class MoveToFrontLinkedList(LinkedList):
    """A linked list implementation that uses a "move to front" heuristic for searches.

    Representation Invariants:
        - all items in this linked list are unique
    """

    def __contains__(self, item: Any) -> bool:
        """Return whether item is in this linked list.

        If the item is found, move it to the front of this list.

        >>> linky = MoveToFrontLinkedList([10, 20, 30, 40, 50, 60])
        >>> linky.__contains__(40)
        True
        >>> linky.to_list()
        [40, 10, 20, 30, 50, 60]
        >>> linky.__contains__(65)
        False
        >>> linky.__contains__(20)
        True
        >>> linky.to_list()
        [20, 40, 10, 30, 50, 60]
        >>> linky.__contains__(60)
        True
        >>> linky.to_list()
        [60, 20, 40, 10, 30, 50]
        """
        prev, curr = None, self._first

        while not (curr is None or curr.item == item):
            prev, curr = curr, curr.next

        assert curr is None or curr.item == item

        if curr is None:
            # Reached the end without finding the item
            return False
        else:
            # found the right node containing the item
            if prev is not None:
                prev.next = curr.next
                node_to_mutate = self._first
                self._first = curr
                self._first.next = node_to_mutate
            return True


################################################################################
# Heuristic 2 (swap)
################################################################################
class SwapLinkedList(LinkedList):
    """A linked list implementation that uses a "swap" heuristic for searches.

    Representation Invariants:
        - all items in this linked list are unique
    """

    def __contains__(self, item: Any) -> bool:
        """Return whether item is in this linked list.

        If the item is found, swap it with the item before it, if any.
        You may do this by reassigning _Node item or next attributes (or both).

        >>> linky = SwapLinkedList([10, 20, 30, 40, 50, 60])
        >>> linky.__contains__(40)
        True
        >>> linky.to_list()
        [10, 20, 40, 30, 50, 60]
        >>> linky.__contains__(65)
        False
        >>> linky.__contains__(20)
        True
        >>> linky.to_list()
        [20, 10, 40, 30, 50, 60]
        >>> linky.__contains__(60)
        True
        >>> linky.to_list()
        [20, 10, 40, 30, 60, 50]
        """
        prev, curr = None, self._first

        while not (curr is None or curr.item == item):
            prev, curr = curr, curr.next

        assert curr is None or curr.item == item

        if curr is None:
            return False
        else:
            if prev is not None:
                # leftward_item_after_swap = curr.item
                # rightward_item_after_swap = prev.item
                # prev.item = leftward_item_after_swap
                # curr.item = rightward_item_after_swap
                prev.item, curr.item = curr.item, prev.item
            return True


################################################################################
# Heuristic 3 (count)
################################################################################
# NOTE: this heuristic requires a new kind of _Node that has an additional "count" attribute.
@dataclass
class _CountNode(_Node):
    """A node in a CountLinkedList.

    Instance Attributes:
      - item: The data stored in this node.
      - next: The next node in the list, if any.
      - access_count: The number of times this node has been accessed (used by the count heuristic)
    """
    next: Optional[_CountNode] = None
    access_count: int = 0


class CountLinkedList(LinkedList):
    """A linked list implementation that uses a "swap" heuristic for searches.

    Representation Invariants:
        - all items in this linked list are unique
    """
    _first: Optional[_CountNode]

    def append(self, item: Any) -> None:
        """Add the given item to the end of this linked list.
        """
        new_node = _CountNode(item)

        if self._first is None:
            self._first = new_node
        else:
            curr = self._first
            while curr.next is not None:
                curr = curr.next

            # After the loop, curr is the last node in the LinkedList.
            assert curr is not None and curr.next is None
            curr.next = new_node

    def __contains__(self, item: Any) -> bool:
        """Return whether item is in this linked list.

        If the item is found, increase its count and reorder the nodes in
        non-increasing count order---see assignment handout for details.

        >>> linky = CountLinkedList([10, 20, 30, 40, 50, 60])
        >>> linky.__contains__(40)
        True
        >>> linky.to_list()
        [40, 10, 20, 30, 50, 60]
        """
        prev, curr = None, self._first

        while not (curr is None or curr.item == item):
            prev, curr = curr, curr.next

        assert curr is None or curr.item == item

        if curr is None:
            return False
        else:
            curr.access_count += 1
            if prev is None:
                # [1 (3), 2 (1), 3 (1)] to [1 (4), 2 (1), 3 (1)]
                return True
            else:
                prev.next = curr.next

                new_prev = None
                following_node = self._first

                while not (following_node is None
                           or following_node.access_count < curr.access_count):
                    new_prev, following_node = following_node, following_node.next

                assert following_node is None or \
                    following_node.access_count < curr.access_count

                if new_prev is None:
                    curr.next = following_node
                    self._first = curr
                    return True
                else:
                    curr.next = following_node
                    new_prev.next = curr
                    return True


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['E1136'],
        'extra-imports': ['a1_linked_list'],
        'max-nested-blocks': 4
    })

    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    import doctest
    doctest.testmod()
