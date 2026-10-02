"""Tests for tree planting algorithms."""

import itertools
import unittest

from tree_planting import plant_trees_backtracking, plant_trees_greedy


class TreePlantingTests(unittest.TestCase):
    def assert_valid_solution(self, tree_count, plots, result):
        possible, positions = result
        self.assertTrue(possible)
        self.assertEqual(len(positions), tree_count)
        occupied = set(index for index, plot in enumerate(plots) if plot == 1)
        occupied.update(positions)
        self.assertEqual(len(occupied), sum(plots) + tree_count)
        self.assertTrue(all(abs(left - right) > 1 for left, right in zip(sorted(occupied), sorted(occupied)[1:])))

    def test_empty_and_zero_count(self):
        self.assertEqual(plant_trees_greedy(0, []), (True, []))
        self.assertEqual(plant_trees_backtracking(0, [1, 0]), (True, []))
        self.assertEqual(plant_trees_greedy(1, []), (False, []))

    def test_boundaries_and_existing_trees(self):
        result = plant_trees_greedy(2, [0, 0, 0, 0, 0])
        self.assert_valid_solution(2, [0, 0, 0, 0, 0], result)
        result = plant_trees_greedy(1, [1, 0, 0])
        self.assert_valid_solution(1, [1, 0, 0], result)

    def test_impossible_request_returns_empty_positions(self):
        self.assertEqual(plant_trees_greedy(2, [0, 0]), (False, []))
        self.assertEqual(plant_trees_backtracking(2, [0, 0]), (False, []))

    def test_input_is_not_modified(self):
        plots = [0, 0, 0]
        plant_trees_greedy(1, plots)
        plant_trees_backtracking(1, plots)
        self.assertEqual(plots, [0, 0, 0])

    def test_invalid_inputs_are_rejected(self):
        cases = [
            (-1, [0]),
            (1.5, [0]),
            (1, [0, 2]),
            (1, [1, 1]),
            (True, [0]),
            (1, [False]),
        ]
        for algorithm in (plant_trees_greedy, plant_trees_backtracking):
            for tree_count, plots in cases:
                with self.subTest(algorithm=algorithm.__name__, tree_count=tree_count, plots=plots):
                    with self.assertRaises(ValueError):
                        algorithm(tree_count, plots)

    def test_exhaustive_short_streets_match(self):
        for length in range(9):
            for plots in itertools.product((0, 1), repeat=length):
                if any(plots[index] == plots[index + 1] == 1 for index in range(length - 1)):
                    continue
                for tree_count in range(length + 2):
                    with self.subTest(plots=plots, tree_count=tree_count):
                        baseline = plant_trees_backtracking(tree_count, plots)
                        proposed = plant_trees_greedy(tree_count, plots)
                        self.assertEqual(proposed[0], baseline[0])
                        if proposed[0]:
                            self.assert_valid_solution(tree_count, plots, proposed)


if __name__ == "__main__":
    unittest.main()