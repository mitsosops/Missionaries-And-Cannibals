import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import graph as g
from math import ceil

# #################### Function declarations #################### #
def a_star(_g, _node, stack = [], steps_to_solution = []):    
    pass

def solve_a_star():
    # #################### Preparation #################### #
    # Build problem graph
    G, root_node = g.problem_graph()

    # Prepare problem graph's plot data 
    pos, color_map, labels = g.prepare_plot_data(G)

    # Create a figure for the problem graph and the result graph
    fig = plt.figure('Cannibals And Missionaries Problem And Solution With DFS', figsize=(20, 10))

    # Set figure title
    fig.suptitle('Cannibals And Missionaries Problem - Network Graphs', fontsize=16)

    # Keep all the axes created in a list for easy switching
    axes = []

    # Create the first subplot for the problem's network graph
    axes += [plt.subplot(1, 2, 1)]

    # Problem graph plot title
    plt.title("All Possible Problem Steps")

    # Use networkx to draw the problem graph on the plot
    g.draw_network(G, pos, color_map, labels, draw_weights=True)

    # #################### Solution #################### #
    pass


if __name__ == "__main__":
    import os
    if not os.path.exists('dist'):
        os.makedirs('dist')
    solve_a_star()
