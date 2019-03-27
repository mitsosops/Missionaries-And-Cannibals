from math import ceil

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

import graph


# #################### Function declarations #################### #


def dfs(_g, _node, stack=None, steps_to_solution=None):
    """
    Run dfs against the passed graph starting with the passed node.

    :param _g: The graph on which to run the dfs.
    :param _node: The node from which this recursion of dfs begins.
    :param stack: The dfs stack. Do not pass this arguments. It is only to be used from the function itself.
    :param steps_to_solution: The steps to solution list. Do not pass this arguments.
                              It is only to be used from the function itself.
    :return: The result path and the steps the algorithm made before reaching the goal node.
    """
    if stack is None:
        stack = []
    if steps_to_solution is None:
        steps_to_solution = []

    stack.append(_node)
    steps_to_solution.append((list(stack), 'stack'))
    node_data = _g.nodes[_node]
    node_data['visited'] = True
    if node_data['is_goal']:
        return stack, steps_to_solution
    elif node_data['is_bad']:
        stack.pop()
        steps_to_solution.append((list(stack), 'pop'))
        return [], steps_to_solution
    else:
        for neighbor in (nb for nb in _g.neighbors(_node) if 'visited' not in _g.nodes[nb].keys()):
            search_result, _ = dfs(_g, neighbor, stack, steps_to_solution)
            if search_result:
                return search_result, steps_to_solution
        stack.pop()
        steps_to_solution.append((list(stack), 'pop'))
        return [], steps_to_solution


def solve_dfs(g, root_node):
    """
    Solve the problem by running a dfs on the provided graph starting from the provided node. Plots the problem graph,
    the result graph (path from root to goal) and the state of the dfs after each iteration.

    :param g: The problem graph.
    :param root_node: The starting node of the graph.
    """
    # #################### Preparation #################### #

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

    # Draw the problem graph on the plot
    graph.draw_network(g, pos, color_map, labels)

    # #################### Solution #################### #
    # Run DFS on the problem graph and keep the search steps in a separate variable for plotting.
    # This implementation of DFS stops traversing the tree when it visits a bad node,
    # where the cannibals end up eating the missionaries, as if it were a leaf node.
    # That means that the bad node is removed from the stack and the traversal continues with its next sibling. It
    # only returns when it finds the solution node, where everyone has crossed the river.
    # This specialized DFS also keeps a track of the traversal steps when adding or popping a node from the stack.
    # Node removals from the stack are tracked in order for the steps to be coherent when plotted side by side
    dfs_result, dfs_states = dfs(g, root_node)

    # The steps are actually the number of unique node visits.
    # It is calculated by counting only the number of stack additions in the resulting states
    # and not the  number of stack removals
    dfs_steps = [s for s in dfs_states if s[1] == 'stack']

    # Make a copy of the problem network and discard the nodes that were not used in the solution
    g_result = graph.filter_graph_copy(g, dfs_result)

    # Prepare plot data for the resulting graph
    pos_result, color_map_result, labels_result = graph.prepare_plot_data(g_result)

    # Since the position of the nodes is calculated based on the number of the nodes per level,
    # remap their position to match the original, which was calculated when preparing the problem's plot data
    pos_result = graph.align_positions(pos, pos_result)

    # Create the second subplot for the result's network graph
    axes += [plt.subplot(1, 2, 2)]

    # Result graph plot title
    plt.title("DFS Result: {} Moves - {} Steps".format(len(dfs_result) - 1, len(dfs_steps)))

    # Draw the result graph on the plot
    graph.draw_network(g_result, pos_result, color_map_result, labels_result)

    # Format the plots' appearance and add a custom legend to them
    graph.clear_axes(axes)
    legend_elements = [Line2D([0], [0], marker='o', color='deepskyblue',
                              label='Starting State', markerfacecolor='deepskyblue', markersize=10),
                       Line2D([0], [0], marker='o', color='gold',
                              label='Valid Move - River crossed safely', markerfacecolor='gold', markersize=10),
                       Line2D([0], [0], marker='o', color='orangered',
                              label='Wrong Move - Missionaries are cannibalized', markerfacecolor='orangered',
                              markersize=10),
                       Line2D([0], [0], marker='o', color='limegreen',
                              label='Solution - Everyone has crossed the river', markerfacecolor='limegreen',
                              markersize=10)]
    graph.add_legend(legend_elements, axes[1], (0.15, 0))

    plt.savefig("dist/DFS_Problem_Solution_Figure.png", bbox_inches='tight')

    # #################### Solution Analysis #################### #
    # Create a new figure for solution step plotting
    fig2 = plt.figure('Cannibals And Missionaries Solution Steps With DFS', figsize=(20, 10))

    # Set figure title
    fig2.suptitle('Cannibals And Missionaries Problem - DFS Solution Steps', fontsize=16)

    # Keep all the axes created in a list for easy switching
    axes2 = []

    # Calculate the number of the required subplot rows and columns based on the number of solution steps
    # Each row should have at most max_cols subplots
    max_cols = 10
    num_of_states = len(dfs_states)
    num_rows = ceil(num_of_states/max_cols)
    num_cols_last_row = num_of_states % max_cols

    # Add a variable for counting pops, this will help track the correct step number
    pop_count = 0
    for r in range(1, num_rows + 1):
        num_cols = max_cols if r < num_rows else num_cols_last_row
        for c in range(1, num_cols + 1):
            # Calculate the index of the subplot which is also the DFS state number
            idx = (r - 1) * max_cols + c

            # Add a subplot for the current state
            axes2 += [plt.subplot(num_rows, max_cols, idx)]

            # Get the nodes that were in the DFS stack at the current state
            state_nodes = dfs_states[idx - 1][0]

            # Get the state type
            state_type = dfs_states[idx - 1][1]

            # If the state type is 'pop' then increase the pop counter
            pop_count += 1 if state_type == 'pop' else 0

            # Name the subplot.
            # Subtracting the pop count from the state number (idx) results in the actual DFS step number
            plt.title('Step ' + str(idx - pop_count) + ('(pop)' if state_type == 'pop' else ''))

            # Copy the problem graph but filter out the nodes that were not included in the current state
            g_state = graph.filter_graph_copy(g, state_nodes)

            # Prepare plot data for the current state
            pos_state, color_map_state, labels_state = graph.prepare_plot_data(g_state)

            # Reset node positions to match the problem graph
            pos_state = graph.align_positions(pos, pos_state)

            # Draw the state graph using smaller node and font sizes
            graph.draw_network(g_state, pos_state, color_map_state, labels_state, node_size=250, font_size=6)

    # Remove ticks from the axes
    graph.clear_axes(axes2)

    plt.savefig("dist/DFS_Solution_Steps_Figure.png", bbox_inches='tight')


if __name__ == "__main__":
    import os
    if not os.path.exists('dist'):
        os.makedirs('dist')
    solve_dfs(*graph.problem_graph())
