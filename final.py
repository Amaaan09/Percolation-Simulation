import streamlit as st
import numpy as np
from percolation import WeightedTree
import plotly.graph_objs as go

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
    percolates = tree.find(source) == tree.find(sink)

    # Create a Plotly visualization of the percolation grid
    data = [
        go.Heatmap(
            z=grid,
            colorscale=[[0, '#FFFFFF'], [1, '#000000']],
            showscale=False
        )
    ]
    layout = go.Layout(
        width=600,
        height=600,
        xaxis=dict(
            ticks='',
            showticklabels=False
        ),
        yaxis=dict(
            ticks='',
            showticklabels=False
        ),
        margin=dict(t=0, l=0, r=0, b=0),
        title=dict(text=f'Percolation Grid (n={n}, p={p})')
    )
    fig = go.Figure(data=data, layout=layout)

    return percolates, fig

st.title('Percolation Simulation')

n = st.sidebar.slider('Grid Size', 10, 100, 50, step=10)
p = st.sidebar.slider('Occupation Probability', 0.0, 1.0, 0.5, 0.05)

if st.button('Run Simulation'):
    result, fig = percolation(n, p)
    if result:
        st.success('The grid percolates!')
    else:
        st.error('The grid does not percolate.')
    st.plotly_chart(fig)
