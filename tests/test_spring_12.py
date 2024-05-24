from spring_12 import Node, Condition, get_num_arangements

N = Node


def test_1():
    assert get_num_arangements([], [], 1, False) == 0
    assert get_num_arangements([], [], 0, False) == 1


def test_2():
    nodes = [
        Node(3, Condition.UNKNOWN),
        Node(1, Condition.UNBROKEN),
        Node(3, Condition.BROKEN),
    ]

    assert get_num_arangements(nodes, [1, 1, 3], 0, False) == 1
