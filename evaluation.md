# Implementation and Evaluation

## Implementation and Testing

The file tree_planting.py contains both algorithms. Each returns True and the new planting positions when there is enough room, or False and an empty list when there is not. Both leave the original street unchanged. They also raise ValueError for inputs such as a negative tree count or a starting street with trees next to each other.

The six tests check empty streets, requests for zero trees, plots at the ends of the street, impossible requests, invalid inputs, and whether the original list stays unchanged. They also compare both algorithms on every valid street of up to eight plots. For each street, the requested number of trees ranges from zero through $P+1$, where $P$ is the number of plots. When greedy returns positions, the tests check that those positions follow the planting rule. All six tests passed.

Run the tests with:

```text
python -m unittest -v
```

## Benchmarking

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

## Findings

The difference between the algorithms grew as we added more plots. At 8 plots, greedy took about 91.98% less time. At 32 plots, the baseline took about 6.67 seconds, while greedy took about 0.00000804 seconds. That is a time reduction of about 99.9999%. Going from 28 to 32 plots made the baseline take about 6.1 times as long. We stopped at 32 because the three baseline runs at that size already took about 20 seconds, and the search was getting much slower.

These results support our running time comparison. The baseline tries many groups of positions, while greedy checks the street once. Greedy was much faster on all seven sizes. Its times are very small, so small timing changes can keep them from rising smoothly. This experiment only uses empty streets where the request is impossible. It does not tell us how the algorithms perform on every input. A next step would be to test requests that can be completed and streets that already have trees.
