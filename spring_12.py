from enum import StrEnum
from dataclasses import dataclass


class Condition(StrEnum):
    UNKNOWN = "?"
    BROKEN = "#"
    UNBROKEN = "."


@dataclass
class Node:
    count: int
    condition: Condition


def get_num_arangements(
    nodes: list[Node],
    broken_counts: list[int],
    missing_broken_count: int,
    last_node_broken: bool,
) -> int:
    if len(nodes) == 0:
        if missing_broken_count == 0 and len(broken_counts) == 0:
            return 1
        else:
            return 0
    if missing_broken_count == 0 and len(broken_counts) == 0:
        if any([n.condition == Condition.BROKEN for n in nodes]):
            return 0
        else:
            return 1

    head = nodes[0]

    match head.condition:
        case Condition.BROKEN:
            if missing_broken_count > 0:
                if head.count <= missing_broken_count:
                    return get_num_arangements(
                        nodes[1:],
                        broken_counts,
                        missing_broken_count - head.count,
                        True,
                    )
                else:
                    return 0
            else:
                if last_node_broken:
                    return 0
                if head.count <= broken_counts[0]:
                    return get_num_arangements(
                        nodes[1:],
                        broken_counts[1:],
                        broken_counts[0] - head.count,
                        True,
                    )
                else:
                    return 0
        case Condition.UNBROKEN:
            if missing_broken_count > 0:
                return 0
            else:
                return get_num_arangements(nodes[1:], broken_counts, 0, False)
        case Condition.UNKNOWN:
            if missing_broken_count > 0:
                if head.count <= missing_broken_count:
                    return get_num_arangements(
                        nodes[1:],
                        broken_counts,
                        missing_broken_count - head.count,
                        True,
                    )
                else:
                    new_unknown_count = head.count - missing_broken_count
                    return get_num_arangements(
                        [Node(new_unknown_count, Condition.UNKNOWN)] + nodes[1:],
                        broken_counts,
                        0,
                        True,
                    )
            else:
                if last_node_broken:
                    return get_num_arangements(
                        [Node(head.count - 1, Condition.UNKNOWN)] + nodes[1:],
                        broken_counts,
                        0,
                        False,
                    )
                else:
                    if head.count <= broken_counts[0]:
                        return get_num_arangements(
                            nodes[1:],
                            broken_counts[1:],
                            broken_counts[0] - head.count,
                            True,
                        )
                    else:
                        total_count = 0
                        for i in range(0, head.count + 1):
                            new_unknown_count = head.count - i - broken_counts[0]
                            if new_unknown_count <= 0:
                                new_nodes = nodes[1:]
                                new_missing_broken_count = -new_unknown_count
                                last_node_broken = True
                            else:
                                new_nodes = [
                                    Node(new_unknown_count, Condition.UNKNOWN)
                                ] + nodes[1:]
                                new_missing_broken_count = 0
                                last_node_broken = False
                            total_count += get_num_arangements(
                                new_nodes,
                                broken_counts[1:],
                                new_missing_broken_count,
                                last_node_broken,
                            )

                        return total_count
