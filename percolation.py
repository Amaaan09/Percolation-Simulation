import numpy as np
import random

def percolates_DFS(n, p):
    # initialize the grid with blocked sites
    grid = [[0 for i in range(n)] for j in range(n)]

    # populate the grid with open sites
    for i in range(n):
        for j in range(n):
            if random.random() < p:
                grid[i][j] = 1

    # initialize a variable to keep track of visited sites
    visited = [[False for i in range(n)] for j in range(n)]

    # initialize a count variable for the number of open sites
    count = 0

    # perform recursive DFS on each open site in the top row
    for j in range(n):
        if grid[0][j] == 1:
            dfs(grid, visited, count, 0, j)

    # check if any site in the bottom row is connected to the top row
    for j in range(n):
        if visited[n-1][j]:
            return True, count

    return False, count

def dfs(grid, visited, count, i, j):
    # mark the site as visited
    visited[i][j] = True

    # increment the count of open sites
    count += 1

    # check the neighboring sites
    if i > 0 and grid[i-1][j] == 1 and not visited[i-1][j]:
        dfs(grid, visited, count, i-1, j)
    if i < len(grid)-1 and grid[i+1][j] == 1 and not visited[i+1][j]:
        dfs(grid, visited, count, i+1, j)
    if j > 0 and grid[i][j-1] == 1 and not visited[i][j-1]:
        dfs(grid, visited, count, i, j-1)
    if j < len(grid)-1 and grid[i][j+1] == 1 and not visited[i][j+1]:
        dfs(grid, visited, count, i, j+1)

class WeightedTree:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, i):
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            if self.size[root_i] < self.size[root_j]:
                root_i, root_j = root_j, root_i
            self.parent[root_j] = root_i
            self.size[root_i] += self.size[root_j]

def percolates_WT(n, p):
    # Initialize the grid
    grid = np.random.rand(n, n) < p

    # Initialize the tree
    tree = WeightedTree(n * n + 2)
    source = n * n
    sink = n * n + 1

    # Connect the source to the top row and the sink to the bottom row
    for j in range(n):
        if grid[0][j]:
            tree.union(source, j)
        if grid[n-1][j]:
            tree.union(sink, (n-1)*n+j)

    # Connect adjacent occupied sites in the grid
    for i in range(n):
        for j in range(n):
            if grid[i][j]:
                index = i * n + j
                if i > 0 and grid[i-1][j]:
                    tree.union(index, (i-1)*n+j)
                if j > 0 and grid[i][j-1]:
                    tree.union(index, i*n+j-1)
                if i < n-1 and grid[i+1][j]:
                    tree.union(index, (i+1)*n+j)
                if j < n-1 and grid[i][j+1]:
                    tree.union(index, i*n+j+1)

    # Check if the source and sink are connected
    return tree.find(source) == tree.find(sink)
