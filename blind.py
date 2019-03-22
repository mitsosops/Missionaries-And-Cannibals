import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import graph as g
from math import ceil

# #################### Function declarations #################### #
def DFS(_g, _node, stack = [], steps_to_solution = []):    
    stack.append(_node)
    steps_to_solution.append((list(stack), 'stack'))
    node_data = _g.nodes[_node]
    node_data['visited'] = True
    if node_data['is_goal']:
        return stack, steps_to_solution
    elif node_data['is_final']:
        stack.pop()
        steps_to_solution.append((list(stack), 'pop'))
        return [], steps_to_solution
    else:
        for neighbor in (nb for nb in _g.neighbors(_node) if 'visited' not in _g.nodes[nb].keys()):
            search_result, _ = DFS(_g, neighbor, stack, steps_to_solution)
            if search_result != []:
                return search_result, steps_to_solution
        stack.pop()
        steps_to_solution.append((list(stack), 'pop'))
        return [], steps_to_solution

def blind():
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
    g.draw_network(G, pos, color_map, labels)

    # #################### Solution #################### #
    # Run DFS on the problem graph and keep the search steps in a separate variable for plotting
    # This implementation of DFS stops traversing the tree when it visits a bad node, where the cannibals end up eating the missionaries,
    # as if it were a leaf node. That means that the bad node is removed from the stack and the traversal continues with its next sibling. It
    # only returns when it finds the solution node, where everyone has crossed the river.
    # This specialized DFS also keeps a track of the traversal steps when adding or popping a node from the stack. Node removals from the stack
    # are tracked in order for the steps to be coherent when plotted side by side
    dfs_result, dfs_states = DFS(G, root_node)

    # The steps are actually the number of unique node visits. It is calculated by counting only the number of stack additions in the resulting states
    # and not the  number of stack removals
    dfs_steps = [s for s in dfs_states if s[1] == 'stack']

    # Make a copy of the problem network and discard the nodes that were not used in the solution
    G_result = g.filter_graph_copy(G, dfs_result)

    # Prepare plot data for the resulting graph
    pos_result, color_map_result, labels_result = g.prepare_plot_data(G_result) 

    # Since the position of the nodes is calculated based on the number of the nodes per level,
    # remap their position to match the original, which was calculated when preparing the problem's plot data
    pos_result = g.align_positions(pos, pos_result)

    # Create the second subplot for the result's network graph
    axes += [plt.subplot(1, 2, 2)]

    # Result graph plot title
    plt.title("DFS Result: " + str(len(dfs_result) - 1) + " Moves - " + str(len(dfs_steps)) + " Steps")

    # Use networkx to draw the result graph on the plot
    g.draw_network(G_result, pos_result, color_map_result, labels_result)

    # Format the plots' appearance and add a custom legend to them
    g.clear_axes(axes)        
    legend_elements = [Line2D([0], [0], marker='o', color='deepskyblue', label='Starting State', markerfacecolor='deepskyblue', markersize=10),
                    Line2D([0], [0], marker='o', color='gold', label='Valid Move - River crossed safely', markerfacecolor='gold', markersize=10),
                    Line2D([0], [0], marker='o', color='orangered', label='Wrong Move - Missionaries are cannibalized', markerfacecolor='orangered', markersize=10),
                    Line2D([0], [0], marker='o', color='limegreen', label='Solution - Everyone has crossed the river', markerfacecolor='limegreen', markersize=10)]
    g.add_legend(legend_elements, axes[1],(0.15, 0))

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
    num_of_states = len(dfs_states)
    nrows = ceil(num_of_states/max_ncols)
    ncols_last_row = num_of_states % max_ncols

    # Add a variable for counting pops, this will help track the correct step number
    pop_count = 0
    for r in range(1, nrows + 1):
        ncols = max_ncols if r < nrows else ncols_last_row
        for c in range(1, ncols + 1):
            # Calculate the index of the subplot which is also the DFS state number
            idx = (r - 1) * max_ncols + c

            # Add a sublpot for the current state
            axes2 += [plt.subplot(nrows, max_ncols, idx)]

            # Get the nodes that were in the DFS stach at the current state
            state_nodes = dfs_states[idx - 1][0]

            # Get the state type
            state_type = dfs_states[idx - 1][1]

            # If the state type is 'pop' then increase the pop counter
            pop_count += 1 if state_type == 'pop' else 0

            # Name the subplot. Substracting the pop count from the state number (idx) results in the actual DFS step number
            plt.title('Step ' + str(idx - pop_count) + ('(pop)' if state_type == 'pop' else ''))

            # Copy the problem graph but filter out the nodes that were not included in the current state
            G_state = g.filter_graph_copy(G, state_nodes)

            # Prepare plot data for the current state
            pos_state, color_map_state, labels_state = g.prepare_plot_data(G_state)

            # Reset node positions to match the problem graph
            pos_state = g.align_positions(pos, pos_state)

            # Draw the state graph using smaller node and font sizes
            g.draw_network(G_state, pos_state, color_map_state, labels_state,node_size=250, font_size=6)

    g.clear_axes(axes2)

    plt.savefig("dist/DFS_Solution_Steps_Figure.png", bbox_inches='tight')


if __name__ == "__main__":
    import os
    if not os.path.exists('dist'):
        os.makedirs('dist')
    blind()
