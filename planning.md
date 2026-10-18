# Planning and Analysis

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
