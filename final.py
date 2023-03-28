import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from percolation import percolates_DFS, percolates_WT

st.title('Percolation Simulation')

n = st.sidebar.slider('Grid Size', 10, 100, 50, step=10)
p = st.sidebar.slider('Occupation Probability', 0.0, 1.0, 0.5, 0.05)
percolation = st.sidebar.selectbox('Percolation Algorithm', ['DFS', 'Weighted Tree'])

if st.button('Run Simulation'):
    if percolation == 'DFS':
        grid, percolates, count = percolates_DFS(n, p)
    else:
        grid, percolates, count = percolates_WT(n, p)

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
