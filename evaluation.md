# Implementation and Evaluation

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
