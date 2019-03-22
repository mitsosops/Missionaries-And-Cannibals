import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from graph import (problem_graph,
                   prepare_plot_data,
                   filter_graph_copy,
                   align_positions)
from math import ceil

# #################### Function declarations #################### #
def DFS(_g, _node, stack = [], steps_to_solution = []):    
    stack.append(_node)
    steps_to_solution.append(list(stack))
    node_data = _g.nodes[_node]
    node_data['visited'] = True
    if node_data['is_result']:
        return stack, steps_to_solution
    elif node_data['is_final']:
        stack.pop()
        steps_to_solution.append(list(stack))
        return [], steps_to_solution
    else:
        for neighbor in (nb for nb in _g.neighbors(_node) if 'visited' not in _g.nodes[nb].keys()):
            search_result, _ = DFS(_g, neighbor, stack, steps_to_solution)
            if search_result != []:
                return search_result, steps_to_solution
        stack.pop()
        steps_to_solution.append(list(stack))
        return [], steps_to_solution

def clear_axes(axes):
    for ax in axes:
        ax.set_xticks([])
        ax.set_yticks([])

def add_legend(axis, pos):        
    legend_elements = [Line2D([0], [0], marker='o', color='deepskyblue', label='Starting State', markerfacecolor='deepskyblue', markersize=10),
                    Line2D([0], [0], marker='o', color='gold', label='Valid Move - River crossed safely', markerfacecolor='gold', markersize=10),
                    Line2D([0], [0], marker='o', color='orangered', label='Wrong Move - Missionaries are cannibalized', markerfacecolor='orangered', markersize=10),
                    Line2D([0], [0], marker='o', color='limegreen', label='Solution - Everyone has crossed the river', markerfacecolor='limegreen', markersize=10)]

    axis.legend(handles=legend_elements, bbox_to_anchor=pos)


def draw_network(_g, pos, color_map, labels, node_size=1250, font_size=8):
    nx.draw_networkx_nodes(_g, pos, node_color=color_map, node_size=node_size)
    nx.draw_networkx_edges(_g, pos, alpha=0.2)
    nx.draw_networkx_labels(_g, pos, labels, font_size=font_size)

def blind():
    # #################### Preparation #################### #
    # Build problem graph
    G, root_node = problem_graph()

    # Prepare problem graph's plot data 
    pos, color_map, labels = prepare_plot_data(G)

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
    draw_network(G, pos, color_map, labels)

    # #################### Solution #################### #
    # Run DFS on the problem graph and keep the search steps in a separate variable for plotting
    # This implementation of DFS stops traversing the tree when it visits a bad node, where the cannibals end up eating the missionaries,
    # as if it were a leaf node. That means that the bad node is removed from the stack and the traversal continues with its next sibling. It
    # only returns when it finds the solution node, where everyone has crossed the river.
    # This specialized DFS also keeps a track of the traversal steps when adding or popping a node from the stack. Node removals from the stack
    # are tracked in order for the steps to be coherent when plotted side by side
    dfs_result, dfs_steps = DFS(G, root_node)

    # Make a copy of the problem network and discard the nodes that were not used in the solution
    G_result = filter_graph_copy(G, dfs_result)

    # Prepare plot data for the resulting graph
    pos_result, color_map_result, labels_result = prepare_plot_data(G_result) 

    # Since the position of the nodes is calculated based on the number of the nodes per level,
    # remap their position to match the original, which was calculated when preparing the problem's plot data
    pos_result = align_positions(pos, pos_result)

    # Create the second subplot for the result's network graph
    axes += [plt.subplot(1, 2, 2)]

    # Result graph plot title
    plt.title("DFS Result: " + str(len(dfs_result) - 1) + " Moves")

    # Use networkx to draw the result graph on the plot
    draw_network(G_result, pos_result, color_map_result, labels_result)

    # Format the plots' appearance and add a custom legend to them
    clear_axes(axes)
    add_legend(axes[1],(0.15, 0))

    plt.savefig("dist/DFS_Problem_Solution_Figure.png", bbox_inches='tight')

    # #################### Solution Analysis #################### #
    # Create a new figure for solution step plotting
    fig2 = plt.figure('Cannibals And Missionaries Solution Steps With DFS', figsize=(20, 10))

    # Set figure title
    fig2.suptitle('Cannibals And Missionaries Problem - DFS Solution Steps', fontsize=16)

    # Keep all the axes created in a list for easy switching
    axes2 = []

    # Calculate the number of the required subplot rows and columns based on the number of solution steps
    # Each row should have at most max_ncols subplots
    max_ncols = 10
    num_of_steps = len(dfs_steps)
    nrows = ceil(num_of_steps/max_ncols)
    ncols_last_row = num_of_steps % max_ncols

    for r in range(1, nrows + 1):
        ncols = max_ncols if r < nrows else ncols_last_row
        for c in range(1, ncols + 1):
            # Calculate the index of the subplot which is also the DFS step number
            idx = (r - 1) * max_ncols + c

            # Add a sublpot for the current step
            axes2 += [plt.subplot(nrows, max_ncols, idx)]

            # Name the subplot
            plt.title('Step ' + str(idx))

            # Get the nodes that were in the DFS stach at the current step
            step_nodes = dfs_steps[idx - 1]

            # Copy the problem graph but filter out the nodes that were not included in the current step
            G_step = filter_graph_copy(G, step_nodes)

            # Prepare plot data for the current step
            pos_step, color_map_step, labels_step = prepare_plot_data(G_step)

            # Reset node positions to match the problem graph
            pos_step = align_positions(pos, pos_step)

            # Draw the step graph using smaller node and font sizes
            draw_network(G_step, pos_step, color_map_step, labels_step,node_size=250, font_size=6)

    clear_axes(axes2)

    plt.savefig("dist/DFS_Solution_Steps_Figure.png", bbox_inches='tight')

if __name__ == "__main__":
    import os
    if not os.path.exists('dist'):
        os.makedirs('dist')
    blind()
