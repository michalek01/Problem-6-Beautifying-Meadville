# Planting Trees Problem

This report compares two ways to find places for new trees in Meadville. We explain both algorithms, compare their running times, and discuss the test and timing results.

## Problem Formulation

We want to find out whether we can plant $N$ new trees along a street in Meadville without putting any two trees next to each other. The street is a list of plots, where 1 means a tree is already there and 0 means the plot is empty. We assume the starting street follows this rule and $N$ is a nonnegative integer. The first and last plots have only one neighbor.

The input is $N$ and the list of plots. If enough trees can be planted, the output is True and a list of their positions, starting at position 0. Otherwise, the output is False and an empty list. For example, with plots [1, 0, 0, 0, 1] and $N=1$, we can plant at position 2. If $N=2$, there is not enough room. Both algorithms leave the original list unchanged.

## Baseline Solution

Our baseline tries different groups of empty plots. It uses backtracking, which means trying a choice and returning to other choices if it does not lead to a solution. A stack keeps track of the groups we still need to try. Each group stores the positions chosen so far and where to start looking next, so we do not try the same group in different orders.

For each group, we look for another empty plot that is not next to an existing tree or a tree already chosen. We add each valid choice to the stack and keep searching until a group contains $N$ positions. If the stack becomes empty, none of the groups worked. This approach is straightforward, but it can take a long time because it explores many possible groups.

```text
ALGORITHM PlantTreesBaseline(N, plots)
    empty_positions ← positions of all empty plots
    stack ← an empty stack
    PUSH (empty list, 0) onto stack

    WHILE stack is not empty
        (chosen, start) ← POP from stack
        IF number of chosen positions = N
            RETURN (True, chosen)

        FOR each entry j in empty_positions, starting at start
            position ← empty_positions[j]
            IF no existing neighbor of position contains a tree
               AND position is not next to any position in chosen
                next_choices ← a copy of chosen with position added
                PUSH (next_choices, j + 1) onto stack

    RETURN (False, empty list)
```

## Proposed Algorithmic Strategy

The proposed algorithm uses a greedy strategy. It goes from left to right and plants a tree at the first available plot whose neighbors are empty. It records that position and marks the plot as occupied in a copy of the street. This prevents it from planting in the next plot. It stops when it has planted $N$ trees or checked the whole street.

Choosing the earliest valid plot leaves at least as much room on the right as choosing a later plot. If a solution plants its first new tree later, we can move that tree to the earliest valid plot without putting it next to an existing tree or the next new tree. We can repeat this reasoning for the remaining plots. This is why the greedy algorithm can find enough positions whenever a valid solution exists.

```text
ALGORITHM PlantTreesGreedy(N, plots)
    working_plots ← a copy of plots
    chosen ← an empty list
    IF N = 0
        RETURN (True, chosen)

    FOR each position from left to right in working_plots
        IF this plot is empty
           AND every neighbor that exists is empty
            Mark this plot as occupied in working_plots
            Add this position to chosen
            IF number of chosen positions = N
                RETURN (True, chosen)

    RETURN (False, empty list)
```

## Complexity Analysis

Let $P$ be the total number of plots. We use this same input size to compare both algorithms. The baseline searches groups of empty plots, and there are at most $2^P$ possible groups. For each group, it may check up to $P$ candidates and compare each one with up to $P$ chosen positions. This gives a worst case upper bound of $O(P^2 2^P)$. Not every group is valid or explored, so this is an upper bound rather than an exact count. The main issue is that the search can grow exponentially as the street gets longer.

The greedy algorithm copies the street and checks each plot once. At each plot, it checks at most two neighbors, which takes constant time. Its running time is $\Theta(P)$. Unlike the baseline, it does not search different groups of positions, so it scales much better as the number of plots increases.

## Empirical Evaluation

### Implementation and Testing

The file tree_planting.py contains both algorithms. Each returns True and the new planting positions when the request is possible, or False and an empty list when it is not. Both keep the original street unchanged and raise ValueError for invalid inputs, such as a negative tree count or adjacent existing trees.

We checked empty streets, requests for zero trees, plots at the ends of the street, impossible requests, and whether the input stays unchanged. The tests also compare both algorithms on every valid street of up to eight plots, with requested counts from zero through $P+1$. For each successful greedy result, they check that the returned positions follow the planting rule. All six tests passed in the new run.

Run the tests with:

```text
python -m unittest -v
```

### Benchmarking

We expanded the timing experiment from five street sizes to seven, adding 28 and 32 plots. Each street starts empty, and we request $P/2+1$ trees for these even street sizes. At most $P/2$ trees can fit, so both algorithms must report failure. This makes the baseline finish searching rather than stop after finding an early solution. Each time below is the median of three runs from a fresh run in the same environment.

Run the timing script with:

```text
python benchmark.py
```

| Plots | Trees requested | Baseline time (seconds) | Greedy time (seconds) | Time reduction |
| --- | --- | --- | --- | --- |
| 8 | 5 | 0.000056666 | 0.000004687 | 91.7287% |
| 12 | 7 | 0.000309218 | 0.000003655 | 98.8180% |
| 16 | 9 | 0.002542734 | 0.000005008 | 99.8030% |
| 20 | 11 | 0.016508224 | 0.000006410 | 99.9612% |
| 24 | 13 | 0.124132768 | 0.000006941 | 99.9944% |
| 28 | 15 | 0.896496264 | 0.000008062 | 99.9991% |
| 32 | 17 | 6.943232570 | 0.000008543 | 99.9999% |

We calculate the percent reduction in time using:

$
\text{Time reduction} = \frac{\text{Baseline time} - \text{Greedy time}}{\text{Baseline time}} \times 100\%
$

### Findings

The gap between the algorithms became much larger as the street grew. At 8 plots, greedy reduced the measured time by about 91.73%. At 32 plots, the baseline took about 6.94 seconds while greedy took about 0.00000854 seconds, a reduction of about 99.9999%. Adding four plots from 28 to 32 made the baseline take about 7.7 times as long. We stopped at 32 because three baseline runs at that size already took about 21 seconds, and the search time was rising quickly.

These results support our expectation that greedy handles longer streets much better. The baseline explores different groups of positions, while greedy only scans the street once. The very short greedy times fluctuate, so the table does not show a smooth increase at every size. This experiment covers impossible requests on empty streets; it does not show how both algorithms behave on every kind of input. A useful next experiment would include possible requests and streets with existing trees.
