# Planting Trees Problem

This report compares two ways to find places for new trees in Meadville. We explain how they work, compare their running times, and discuss the test results.

## Problem Formulation

We want to find out whether we can plant $N$ new trees along a street in Meadville without putting any two trees next to each other. The street is a list of plots. A 1 means a tree is already there, and a 0 means the plot is empty. We assume the starting street follows the planting rule and $N$ is a whole number that is zero or greater. The first and last plots have at most one neighbor. A street with just one plot has no neighbors.

The input is $N$ and the list of plots. If there is enough room, the output is True and the positions where the new trees should go. Positions start at 0. Otherwise, the output is False and an empty list. For example, with plots [1, 0, 0, 0, 1] and $N=1$, we can plant at position 2. If $N=2$, there is not enough room. Both algorithms leave the original list unchanged.

## Baseline Solution

Our baseline tries different groups of empty plots. It uses backtracking, which means trying a choice and going back to try other choices when it does not work. We use a stack to save the groups we still need to check. A stack gives us the most recently added group first. Each saved group includes the positions chosen so far and where to look for the next empty plot.

For each group, we check whether another empty plot is next to an existing tree or a tree we have already chosen. If it is safe, we save a new group with that plot added. We only add positions farther along the street, so we do not repeat the same group in a different order. We stop when a group has $N$ positions. If the stack runs out, there is no valid solution. This method can be slow because it may try many groups before finishing.

```text
ALGORITHM PlantTreesBaseline(N, plots)
    empty_positions ← list of empty plot positions, from left to right
    stack ← an empty stack
    PUSH (empty list, 0) onto stack

    WHILE stack is not empty
        (chosen, start) ← POP from stack
        IF number of chosen positions = N
            RETURN (True, chosen)
        END IF

        FOR each index j from start to the last index of empty_positions
            position ← empty_positions[j]
            IF every neighbor of position that exists in plots is empty
               AND position is not next to any position in chosen
                next_choices ← a copy of chosen with position added
                PUSH (next_choices, j + 1) onto stack
            END IF
        END FOR
    END WHILE

    RETURN (False, empty list)
```

Here, the indices of empty_positions start at 0. If start is past the last index, the FOR loop has nothing to check. A missing neighbor does not block planting.

## Proposed Algorithmic Strategy

The greedy algorithm goes from left to right and plants at the first safe plot. It checks that the plot is empty and that any neighbors are also empty. When it plants a tree, it saves the position and marks the plot as occupied in a copy of the street. This stops it from planting in the next plot. It continues until it has planted $N$ trees or reached the end.

Planting at the earliest safe plot leaves at least as much room on the right as planting farther along. If another solution puts its first new tree later, we can move that tree to the earliest safe plot. It will still be away from existing trees and will be farther from the next new tree. We can use the same reasoning for the remaining trees. This is why greedy finds enough positions whenever a valid solution exists.

```text
ALGORITHM PlantTreesGreedy(N, plots)
    working_plots ← a copy of plots
    chosen ← an empty list

    IF N = 0
        RETURN (True, chosen)
    END IF

    FOR each position from left to right in working_plots
        IF this plot is empty
           AND every neighbor that exists in working_plots is empty
            Mark this plot as occupied in working_plots
            Add this position to chosen
            IF number of chosen positions = N
                RETURN (True, chosen)
            END IF
        END IF
    END FOR

    RETURN (False, empty list)
```

## Complexity Analysis

Let $P$ be the total number of plots. We use $P$ for both algorithms so we can compare them directly. The baseline can consider at most $2^P$ groups. For each group, it can check up to $P$ possible next plots. Checking each choice and copying the chosen positions can take up to $O(P)$ time. A worst case upper bound is therefore $O(P^2 2^P)$. This is a limit on the running time, not an exact count. Many groups are skipped because they would put trees next to each other, but the search can still grow exponentially.

The greedy algorithm copies the street and checks each plot at most once. Each plot only needs up to two neighbor checks, so its worst case running time is $\Theta(P)$. Its work grows with the number of plots, while the baseline may search many different groups. This makes greedy the better choice for longer streets.

## Empirical Evaluation

### Implementation and Testing

The file tree_planting.py contains both algorithms. Each returns True and the new planting positions when there is enough room, or False and an empty list when there is not. Both leave the original street unchanged. They also raise ValueError for inputs such as a negative tree count or a starting street with trees next to each other.

The six tests check empty streets, requests for zero trees, plots at the ends of the street, impossible requests, invalid inputs, and whether the original list stays unchanged. They also compare both algorithms on every valid street of up to eight plots. For each street, the requested number of trees ranges from zero through $P+1$, where $P$ is the number of plots. When greedy returns positions, the tests check that those positions follow the planting rule. All six tests passed.

Run the tests with:

```text
python -m unittest -v
```

### Benchmarking

We tested seven street sizes, from 8 to 32 plots. Each street starts empty. Since all the sizes are even, at most $P/2$ trees can fit. We request $P/2+1$ trees, which is one too many. This makes the baseline search all its valid groups before reporting failure, while greedy only needs one scan. We ran each algorithm three times for each size and used the middle time, or median. The table shows the latest run of benchmark.py.

Run the timing script with:

```text
python benchmark.py
```

| Plots | Trees requested | Baseline time (seconds) | Greedy time (seconds) | Time reduction |
| --- | --- | --- | --- | --- |
| 8 | 5 | 0.000044337 | 0.000003556 | 91.9796% |
| 12 | 7 | 0.000351041 | 0.000003766 | 98.9272% |
| 16 | 9 | 0.002367580 | 0.000004417 | 99.8134% |
| 20 | 11 | 0.018876965 | 0.000006109 | 99.9676% |
| 24 | 13 | 0.144038428 | 0.000006880 | 99.9952% |
| 28 | 15 | 1.087057701 | 0.000007831 | 99.9993% |
| 32 | 17 | 6.665829664 | 0.000008042 | 99.9999% |

To find the percent reduction, we subtract the greedy time from the baseline time, divide by the baseline time, and multiply by 100.

```math
\text{Time reduction} = \frac{\text{Baseline time} - \text{Greedy time}}{\text{Baseline time}} \times 100\%
```

### Findings

The difference between the algorithms grew as we added more plots. At 8 plots, greedy took about 91.98% less time. At 32 plots, the baseline took about 6.67 seconds, while greedy took about 0.00000804 seconds. That is a time reduction of about 99.9999%. Going from 28 to 32 plots made the baseline take about 6.1 times as long. We stopped at 32 because the three baseline runs at that size already took about 20 seconds, and the search was getting much slower.

These results support our running time comparison. The baseline tries many groups of positions, while greedy checks the street once. Greedy was much faster on all seven sizes. Its times are very small, so small timing changes can keep them from rising smoothly. This experiment only uses empty streets where the request is impossible. It does not tell us how the algorithms perform on every input. A next step would be to test requests that can be completed and streets that already have trees.
