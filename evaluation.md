# Deliverable 2: Implementation and Evaluation

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