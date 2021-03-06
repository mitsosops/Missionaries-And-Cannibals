from math import ceil

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

import graph


# #################### Function declarations #################### #

def heuristic(_g, _node, scale=1.0):
    """
    Heuristic function that returns the min distance between the passed node and the goal.

    :param _g: The graph whose nodes to calculate the heuristic for.
    :param _node: The node whose heuristic to calculate.
    :param scale: The scale is used to set the importance of the heuristic function (h(n))
                  when calculating the estimated distance to goal (f(n))
                  against the cost - distance from start (g(n))
    :return: The min weight of the supplied node's adjacent edges which is the shortest distance to the end
    """

    if _g.nodes[_node]['is_goal']:
        return 0
    return min([edge[2]['weight'] for edge in _g.edges(_node, data=True)]) * scale


def a_star(_g, _node):
    """
    Run A* against the passed graph starting with the passed node.

    :param _g: The graph on which to run the dfs.
    :param _node: The node from which the A* search begins.
    :return: The result path and the steps the algorithm made before reaching the goal node.
    """
    steps_to_solution = []

    visited = []
    frontier = [_node]
    origins = {}
    distance_from_start = {_node: 0}
    estimated_distance_to_goal = {_node: heuristic(_g, _node)}

    while frontier:
        current_node = sorted(frontier, key=lambda node: estimated_distance_to_goal[node])[0]
        frontier.remove(current_node)

        if _g.nodes[current_node]['is_goal']:
            steps_to_solution.append({'current_node': current_node, 'frontier': list(frontier),
                                      'visited': list(visited)})
            path = [current_node]
            while current_node in origins.keys():
                current_node = origins[current_node]
                path.append(current_node)
            return path, steps_to_solution

        visited.append(current_node)

        for neighbor in _g.neighbors(current_node):
            if _g.nodes[neighbor]['is_bad'] or neighbor in visited:
                continue

            neighbor_distance_from_start = distance_from_start[current_node] + 1

            if neighbor not in frontier:
                frontier.append(neighbor)
            elif neighbor_distance_from_start >= distance_from_start[neighbor]:
                continue

            origins[neighbor] = current_node
            distance_from_start[neighbor] = neighbor_distance_from_start
            # In this problem, most of the time, getting closer to the goal (minimizing straight line distance)
            # is the best path since there are no concave obstacles. Hence, an arbitrary scale of 2 is chosen to
            # make the heuristic twice as important as cost - distance from the start.
            estimated_distance_to_goal[neighbor] = neighbor_distance_from_start + heuristic(_g, neighbor, scale=2)
            
        steps_to_solution.append({'current_node': current_node, 'frontier': list(frontier), 'visited': list(visited)})


def set_a_star_colors(_g, current_node, frontier, visited):
    color_map = []
    for node in _g.nodes:
        if node == current_node:
            color_map.append('dodgerblue')
        elif node in frontier:
            color_map.append('goldenrod')
        elif node in visited:
            color_map.append('greenyellow')
        elif _g.nodes[node]['is_bad']:
            color_map.append('palevioletred')
        else:
            color_map.append('gainsboro')
    
    return color_map


def solve_a_star(g, root_node):
    """
    Solve the problem by running an A* search on the provided graph starting from the provided node.
    Plots the problem graph, the result graph (path from root to goal) and the state of the A* after each iteration.

    :param g: The problem graph.
    :param root_node: The starting node of the graph.
    """
    # #################### Preparation #################### #

    # Prepare problem graph's plot data 
    pos, color_map, labels = graph.prepare_plot_data(g)

    # Create a figure for the problem graph and the result graph
    fig = plt.figure('Cannibals And Missionaries Problem And Solution With A*', figsize=(20, 10))

    # Set figure title
    fig.suptitle('Cannibals And Missionaries Problem - Network Graphs', fontsize=16)

    # Keep all the axes created in a list for easy switching
    axes = []

    # Create the first subplot for the problem's network graph
    axes += [plt.subplot(1, 2, 1)]

    # Problem graph plot title
    plt.title("All Possible Problem Steps")

    # Draw the problem graph on the plot
    graph.draw_network(g, pos, color_map, labels, draw_weights=True)

    # #################### Solution #################### #
    # Run A* on the problem graph and keep the search steps in a separate variable for plotting.
    # This implementation of A* ignores the bad nodes, where the cannibals end up eating the missionaries.
    # The bad nodes are considered obstacles and thus they are never added to the frontier.
    # This implementation of A* uses a scalable straight distance to goal heuristic.
    # Since the graphs for these types of problems are relatively simple,
    # a stronger heuristic usually gives us the best path in the shortest time possible (steps/iterations).
    # Therefore a scale parameter is added to the heuristic function.
    # As for the solution steps, the following information is tracked for each one of them:
    # current node, frontier nodes and visited nodes.
    # This allows us to plot the whole graph verbosely, knowing exactly the state of the A* after each iteration.
    a_star_result, a_star_steps = a_star(g, root_node)

    # Make a copy of the problem network and discard the nodes that were not used in the solution
    g_result = graph.filter_graph_copy(g, a_star_result)

    # Prepare plot data for the resulting graph
    pos_result, color_map_result, labels_result = graph.prepare_plot_data(g_result)

    # Since the position of the nodes is calculated based on the number of the nodes per level,
    # remap their position to match the original, which was calculated when preparing the problem's plot data
    pos_result = graph.align_positions(pos, pos_result)

    # Create the second subplot for the result's network graph
    axes += [plt.subplot(1, 2, 2)]

    # Result graph plot title
    plt.title("A* Result: {} Moves - {} Steps".format(len(a_star_result) - 1, len(a_star_steps)))

    # Draw the result graph on the plot
    graph.draw_network(g_result, pos_result, color_map_result, labels_result)

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
                              markersize=10),
                       Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0,
                                 label="The line numbers show the 'straight-line distance' to the goal")]

    graph.add_legend(legend_elements, axes[1], (0.15, 0))

    plt.savefig("dist/A_Star_Problem_Solution_Figure.png", bbox_inches='tight')

    # #################### Solution Analysis #################### #
    # Create a new figure for solution step plotting
    fig2 = plt.figure('Cannibals And Missionaries Solution Steps With A*', figsize=(20, 10))

    # Set figure title
    fig2.suptitle('Cannibals And Missionaries Problem - A* Solution Steps', fontsize=16)

    # Keep all the axes created in a list for easy switching
    axes2 = []

    # Calculate the number of the required subplot rows and columns based on the number of solution steps
    # Each row should have at most max_cols subplots
    max_cols = 8
    num_of_steps = len(a_star_steps)
    num_rows = ceil(num_of_steps/max_cols)
    num_cols_last_row = num_of_steps % max_cols
    
    for r in range(1, num_rows + 1):
        num_cols = max_cols if r < num_rows else num_cols_last_row
        for c in range(1, num_cols + 1):
            # Calculate the index of the subplot which is also the DFS step number
            idx = (r - 1) * max_cols + c

            # Add a subplot for the current step
            axes2 += [plt.subplot(num_rows, max_cols, idx)]

            # Name the subplot.
            # Subtracting the pop count from the step number (idx) results in the actual DFS step number
            plt.title('Step {}'.format(idx))

            # Get the data of the current step (A* state)
            step_data = a_star_steps[idx - 1]

            # Prepare plot data for the current step
            pos_step, color_map_step, labels_step = graph.prepare_plot_data(g)

            # Create a new color map for our nodes, that better depicts the state of the A* at each step
            color_map_step = set_a_star_colors(g, step_data['current_node'],
                                               step_data['frontier'], step_data['visited'])

            # Draw the step graph using smaller node and font sizes
            graph.draw_network(g, pos_step, color_map_step, labels_step, node_size=250, font_size=6)

    # Add a legend describing the purpose of each color in the new colormap
    graph.clear_axes(axes2)
    legend_elements = [Line2D([0], [0], marker='o', color='gainsboro',
                              label='Unvisited Node', markerfacecolor='gainsboro', markersize=10),
                       Line2D([0], [0], marker='o', color='palevioletred',
                              label='Bad/Ignored Node', markerfacecolor='palevioletred', markersize=10),
                       Line2D([0], [0], marker='o', color='greenyellow',
                              label='Visited Node', markerfacecolor='greenyellow',
                              markersize=10),
                       Line2D([0], [0], marker='o', color='goldenrod',
                              label='Frontier Node', markerfacecolor='goldenrod',
                              markersize=10),
                       Line2D([0], [0], marker='o', color='dodgerblue',
                              label='Current Node', markerfacecolor='dodgerblue',
                              markersize=10)]
    graph.add_legend(legend_elements, axes2[len(axes2) - 1], (1, 0.65))

    plt.savefig("dist/A_Star_Solution_Steps_Figure.png", bbox_inches='tight')


if __name__ == "__main__":
    import os

    if not os.path.exists('dist'):
        os.makedirs('dist')
    solve_a_star(*graph.problem_graph())
