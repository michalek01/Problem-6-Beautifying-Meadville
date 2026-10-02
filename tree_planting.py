"""Algorithms for finding non-adjacent plots for new trees."""

from typing import List, Sequence, Tuple


def _validate_input(tree_count: int, plots: Sequence[int]) -> None:
    """Raise ValueError when the request or starting street is invalid."""
    if not isinstance(tree_count, int) or isinstance(tree_count, bool):
        raise ValueError("tree_count must be a non-negative integer")
    if tree_count < 0:
        raise ValueError("tree_count must be a non-negative integer")
    if any(plot not in (0, 1) or isinstance(plot, bool) for plot in plots):
        raise ValueError("plots must contain only integer 0s and 1s")
    if any(plots[index] == plots[index + 1] == 1 for index in range(len(plots) - 1)):
        raise ValueError("existing trees cannot occupy adjacent plots")


def plant_trees_backtracking(
    tree_count: int, plots: Sequence[int]
) -> Tuple[bool, List[int]]:
    """Find a valid planting using backtracking; return positions or no solution."""
    _validate_input(tree_count, plots)
    if tree_count == 0:
        return True, []

    empty_plots = [index for index, plot in enumerate(plots) if plot == 0]
    stack = [([], 0)]

    while stack:
        positions, start = stack.pop()
        if len(positions) == tree_count:
            return True, positions

        for candidate_index in range(start, len(empty_plots)):
            position = empty_plots[candidate_index]
            if position > 0 and plots[position - 1] == 1:
                continue
            if position + 1 < len(plots) and plots[position + 1] == 1:
                continue
            if any(abs(position - planted) == 1 for planted in positions):
                continue
            stack.append((positions + [position], candidate_index + 1))

    return False, []


def plant_trees_greedy(
    tree_count: int, plots: Sequence[int]
) -> Tuple[bool, List[int]]:
    """Plant from left to right in linear time; return positions or no solution."""
    _validate_input(tree_count, plots)
    if tree_count == 0:
        return True, []

    working_plots = list(plots)
    positions = []

    for index, plot in enumerate(working_plots):
        if plot != 0:
            continue
        left_empty = index == 0 or working_plots[index - 1] == 0
        right_empty = index == len(working_plots) - 1 or working_plots[index + 1] == 0
        if left_empty and right_empty:
            working_plots[index] = 1
            positions.append(index)
            if len(positions) == tree_count:
                return True, positions

    if len(positions) == tree_count:
        return True, positions
    return False, []