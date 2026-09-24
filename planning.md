Planning and Analysis
Problem Formulation
The objective of the Problem 6 is to plant trees along a street in Meadville. These streets are divided into a row of plots and we need to plant N trees into empty lots. There are already lots that have tree in them and two trees cannot be in adjacent plots. The frist and last plots each have only one neighbor. We will be determining whether N new trees can be planted and if they can, return the positions of the plots to plant them in. Our inputs will be the interget N ( the amount of new trees ) and a list of 1s and 0s. 1 means the plot has a tree and 0 means the plot has no tree. 

Our algorithm determines whether N additional trees can be planted in each row of plots. It scans the list or plots and checks whether the plot is empty and if the left and right plots are empty. If this is true the algorithm will index a 1 and plant a tree. This algorithm will continue until we have planted the proper amount of tree ( N). A failed attempt will still index the trees it indexed into but a failed attempt is whether the algorithm planted to correct amount of trees




```python
def plant_trees(N,plots):
    positions = []

    for i in range(len(plots)):
    if len(positions) == N:
    return True,positions

    if plots[i] == 0:
        left_empty = (i == 0 or plots[i-1] == 0)
        right empty = (i == len(plots) - 1 or plots[i + 1] == 0)

        if left_empty and right empty:
            plots[i] = 1
            positions.append(i)

    if len(positions) == N:
        return True, positions

    return False, []
```