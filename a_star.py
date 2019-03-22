import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import graph


# #################### Function declarations #################### #

def heuristic(_g, _node):
    # Get the min weight of the adjacent edges which is the shortest distance to the end
    return min([edge[2]['weight'] for edge in _g.edges(_node, data=True)])


def a_star(_g, _node):
    steps_to_solution = []

    visited = []
    frontier = [_node]
    origins = {}
    distance_from_start = {_node: 0}
    estimated_distance_to_goal = {_node: heuristic(_g, _node)}

    while frontier:
        current_node = sorted(frontier, key=lambda node: estimated_distance_to_goal[node])[0]
        frontier.remove(current_node)

        steps_to_solution.append({'current_node': current_node, 'frontier': frontier, 'visited': visited})

        if _g.nodes[current_node]['is_goal']:
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
            estimated_distance_to_goal[neighbor] = neighbor_distance_from_start + heuristic(_g, neighbor)


def solve_a_star():
    # #################### Preparation #################### #
    # Build problem graph
    g, root_node = graph.problem_graph()

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
    plt.title("A* Result: " + str(len(a_star_steps)) + " Steps")

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
                              markersize=10)]
    graph.add_legend(legend_elements, axes[1], (0.15, 0))

    plt.show()


if __name__ == "__main__":
    import os

    if not os.path.exists('dist'):
        os.makedirs('dist')
    solve_a_star()
