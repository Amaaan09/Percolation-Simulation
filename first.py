import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from percolation import WeightedTree

def percolation(n, p):
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
    count = 0
    for i in range(n):
        for j in range(n):
            if grid[i][j]:
                index = i * n + j
                count += 1
                if i > 0 and grid[i-1][j]:
                    tree.union(index, (i-1)*n+j)
                if j > 0 and grid[i][j-1]:
                    tree.union(index, i*n+j-1)
                if i < n-1 and grid[i+1][j]:
                    tree.union(index, (i+1)*n+j)
                if j < n-1 and grid[i][j+1]:
                    tree.union(index, i*n+j+1)

    # Check if the source and sink are connected
    percolates = tree.find(source) == tree.find(sink)

    return grid, percolates, count

st.title('Percolation Simulation')

n = st.sidebar.slider('Grid Size', 10, 100, 50, step=10)
p = st.sidebar.slider('Occupation Probability', 0.0, 1.0, 0.5, 0.05)

if st.button('Run Simulation'):
    grid, percolates, count = percolation(n, p)

    fig, ax = plt.subplots()
    ax.imshow(grid, cmap='binary')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title('Percolation Grid')

    if percolates:
        st.success('The grid percolates! {} sites opened.'.format(count))
    else:
        st.error('The grid does not percolate. {} sites opened.'.format(count))

    st.pyplot(fig)
