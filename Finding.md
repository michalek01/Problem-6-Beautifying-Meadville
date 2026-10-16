## Planting Trees Problem

This document outlines the problem formulation,baseline solution and algorithmic strategy for the Planting Trees problem. The goal is to efficiently plant trees in Meadville by finding a algorithm that will the proper plots to plant trees.

## Promblem Formulation

The goal of Problem 6 is to plant N new trees along a street in Meadville. The street is a list of plots. A 1 means that a plot already has a tree, and a 0 means that the plot is empty.

No two trees can be in adjacent plots. This rule applies to both the trees already in the list and the new trees that are planted. The first and last plots only have one neighbor.

The input is an integer N and a list of 1s and 0s. The output should say whether N trees can be planted. If it is possible, the algorithm returns the positions where the new trees should be planted. If it is not possible, it returns False and an empty list.



## Baseline Solution

The first algorithm is the baseline solution. It uses backtracking. It first finds all of the empty plots. Then it tries different possible groups of empty plots where trees could be planted.

For each possible plot, the algorithm checks whether it is next to an existing tree or a newly planted tree. If the plot is valid, it adds that position and continues trying more plots. If it finds N valid positions, it returns True and the list of positions. If it cannot find enough valid positions, it returns False and an empty list.

This baseline is simple because it checks many possible choices. However, it can be slow when there are many empty plots.

```python
def plant_trees(N, plots):
    empty = []

    # Find all empty plots
    for i in range(len(plots)):
        if plots[i] == 0:
            empty.append(i)

    # Start with no new trees planted
    stack = [([], 0)]

    while stack:
        positions, start = stack.pop()

        # Check whether enough trees have been planted
        if len(positions) == N:
            return True, positions

        # Try each remaining empty plot
        for j in range(start, len(empty)):
            position = empty[j]
            valid = True

            # Check existing trees
            if position > 0 and plots[position - 1] == 1:
                valid = False

            if position < len(plots) - 1 and plots[position + 1] == 1:
                valid = False

            # Check newly planted trees
            for planted in positions:
                if abs(position - planted) == 1:
                    valid = False

            if valid:
                new_positions = positions + [position]
                stack.append((new_positions, j + 1))

    return False, []
```





## Proposed Algorithmic Strategy

The second algorithm uses a greedy strategy. It looks at the plots from left to right one time.

When it finds an empty plot, it checks the plot on the left and the plot on the right. If both neighboring plots are empty, or if there is no neighbor because the plot is at the beginning or end of the street, the algorithm plants a tree in that plot.

After planting a tree, the algorithm changes that plot to 1. This makes sure the next plot will not be used because trees cannot be next to each other. The algorithm keeps going until it has planted N trees or reaches the end of the list.

The greedy strategy works because planting a tree in the first valid plot does not stop the algorithm from finding valid plots later in the street.

```python
Algorithm PlantTreesGreedy(N, plots):
    input: Integer N, list of plots of length P
    output: Boolean and list of planting positions

    positions = []
    working_plots = copy of plots

    for i = 0 to P - 1:
        if length(positions) == N:
            return True, positions

        if working_plots[i] == 0:
            left_empty =
                (i == 0 OR working_plots[i - 1] == 0)

            right_empty =
                (i == P - 1 OR working_plots[i + 1] == 0)

            if left_empty AND right_empty:
                working_plots[i] = 1
                append i to positions

    if length(positions) == N:
        return True, positions

    return False, []
```

## Complexity Analysis

Let P be the number of plots in the list.

The baseline backtracking algorithm can try many different combinations of empty plots. If there are E empty plots, it can examine up to 2^E possible combinations. Therefore, its worst-case running time is O(2^E). This can be slow when the street has many empty plots.

The greedy algorithm looks at each plot at most one time. For every plot, it only checks the left and right neighbor. Each check takes constant time.

Therefore, the running time of the greedy algorithm is Theta(P). The algorithm copies the list of plots and saves the positions of newly planted trees, so it uses O(P) extra space in the worst case.

The greedy algorithm is much faster than the baseline algorithm for large inputs because it does not try many different combinations of plots.


## Empirircal Evaluation
## Implementation

`tree_planting.py` contains two functions with the same contract: a successful call returns `(True, positions)`, where positions are zero-based plot indices; an unsuccessful request returns `(False, [])`. Both reject negative or non-integer tree counts, plot values other than integer 0 or 1, and starting streets with adjacent existing trees by raising `ValueError`. Neither function modifies its input.

The baseline, `plant_trees_backtracking`, searches combinations of empty plots and can take exponential time in the number of plots. The proposed `plant_trees_greedy` scans from left to right, planting whenever the current plot and its neighbors allow it. It runs in $O(P)$ time and uses $O(P)$ additional space, where $P$ is the street length.

## Testing

Run the tests with:

```text
python -m unittest -v
```

The suite covers boundary cases, valid planting positions, impossible requests, input preservation, invalid inputs, and exhaustive agreement between both algorithms for all valid streets of up to eight plots and requested counts through `P + 1`.

## Benchmarking

Run the timing script with:

```text
python benchmark.py
```

For each size, the script requests more trees than can fit in an all-empty street. This forces backtracking to examine its search space before reporting failure, while the greedy algorithm completes a single scan. The script reports the median of three runs; results vary by computer and Python version.

| Plots | Trees requested | Backtracking (seconds) | Greedy (seconds) |
|---:|---:|---:|---:|
| 8 | 5 | 0.000090600 | 0.000004400 |
| 12 | 7 | 0.000368700 | 0.000004500 |
| 16 | 9 | 0.002223700 | 0.000007600 |
| 20 | 11 | 0.016602500 | 0.000006800 |
| 24 | 13 | 0.126118900 | 0.000012000 |

## Findings

The exhaustive tests check the greedy algorithm's feasibility result against the baseline across every tested input, and validate that returned positions obey the no-adjacent-trees rule. In this run, increasing the all-empty street from 8 to 24 plots increased measured backtracking time from 0.000090600 s to 0.126118900 s; greedy time remained between 0.000004400 s and 0.000012000 s. These are small single-machine measurements, so exact values vary, but the increasing gap is consistent with exponential search versus a linear scan.