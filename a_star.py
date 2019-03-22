import matplotlib.pyplot as plt
import graph


# #################### Function declarations #################### #


def a_star(_g, _node, stack=None, steps_to_solution=None):
    if stack is None:
        stack = []
    if steps_to_solution is None:
        steps_to_solution = []


def solve_a_star():
    # #################### Preparation #################### #
    # Build problem graph
    g, root_node = graph.problem_graph()

    # Prepare problem graph's plot data 
    pos, color_map, labels = graph.prepare_plot_data(g)

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
    graph.draw_network(g, pos, color_map, labels, draw_weights=True)

    # #################### Solution #################### #
    pass


if __name__ == "__main__":
    import os

    if not os.path.exists('dist'):
        os.makedirs('dist')
    solve_a_star()
