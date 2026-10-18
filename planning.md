# Planning and Analysis

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
