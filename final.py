import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from percolation import percolates_BFS, percolates_WT

st.title('Percolation Simulation')

n = st.sidebar.slider('Grid Size', 10, 100, 50, step=10)
p = st.sidebar.slider('Occupation Probability', 0.0, 1.0, 0.5, 0.05)

if st.button('Run Simulation'):
    grid, percolates, count = percolates_BFS(n, p)

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
