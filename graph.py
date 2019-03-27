from copy import deepcopy

import networkx as nx


def problem_graph():
    """
    Builds the problem graph for the Missionaries and Cannibals problem using
    NetworkX. It calculates the node level (recursion level), which is helpful
    when drawing the graph in a tree-like format, along with the straight distance
    of each node to the goal node, which is saved on the next edges of each node
    since each one of them may have multiple paths leading to the goal.

    :return: Tuple containing the problem graph and the root node of the graph
    """
    starting_bank = sorted(['m', 'm', 'm', 'c', 'c', 'c', 'b'])
    ending_bank = []

    operators = sorted([sorted(l) for l in [['m'],
                                            ['c'],
                                            ['m', 'm'],
                                            ['c', 'c'],
                                            ['m', 'c']]])

    def build_node(_starting_bank, _ending_bank):
        """
        Accepts two lists representing the state of each bank and then it sorts them lexicographically and converts them
        to tuples. That way a node that was created by two lists with the same objects inside and irregardless of their
        index will always have the same hash when serialized.

        :param _starting_bank: The list containing a single letter representation of either missionaries (m),
                               cannibals (c) or the boat (b) that are currently waiting on the starting river bank
        :param _ending_bank: The list containing a single letter representation of either missionaries (m),
                            cannibals (c) or the boat (b) that are currently waiting on the destination river bank
        :return: A Tuple representing the state of both banks for this node. The state includes the missionaries and
                 cannibals on each bank, as well as the bank that currently has the boat. The starting bank is always
                 first in the tuple.
        """
        _node = (tuple(sorted(_starting_bank)), tuple(sorted(_ending_bank)))
        return _node

    g = nx.Graph()

    root_node = build_node(starting_bank, ending_bank)

    def cross_river(_starting_bank, _ending_bank, operator):
        """
        It tries applying the provided 'operator' on the bank that currently has the boat
        to create the next node used in the graph as a child of the node represented by these two bank states.

        :param _starting_bank: The list containing a single letter representation of either missionaries (m),
                               cannibals (c) or the boat (b) that are currently waiting on the starting river bank
        :param _ending_bank: The list containing a single letter representation of either missionaries (m),
                             cannibals (c) or the boat (b) that are currently waiting on the destination river bank
        :param operator: The list containing the single letter representations of the people to move
                         from the bank with the boat to the other (e.x. To move one missionary and on cannibal from
                         the bank with the boat to the other the operator is depicted as such: ['c','m']).
        :return: The node the results when applying the operator to the lists provider. If the operator is not
        applicable (e.x. Move one cannibal from the starting bank to the ending bank, while the ending bank has no
        cannibals), None is returned instead.
        """
        bank1 = bank2 = []
        _starting_bank = list(_starting_bank)
        _ending_bank = list(_ending_bank)
        operator = list(operator)

        if 'b' in _starting_bank:
            bank1 = _starting_bank
            bank2 = _ending_bank
        elif 'b' in _ending_bank:
            bank1 = _ending_bank
            bank2 = _starting_bank

        bank1.remove('b')
        bank2.append('b')

        while any(operator):
            op = operator.pop()
            if op in bank1:
                bank1.remove(op)
                bank2.append(op)
            else:
                return None

        return build_node(_starting_bank, _ending_bank)

    def get_flags(_node):
        """
        It counts the elements of each bank and returns 3 flags that show whether the node is a bad one, is the root or
        the goal node. If all flags are false, it means that this node is part of a path that could possibly be the
        solution.

        :param _node: The node representing the current state of the banks.
        :return: A variable that is True if there are more cannibals than missionaries in a bank, indicating that this
                 is a bad node, as well as two variables indicating whether the starting bank is empty meaning that this
                 is the goal_node, or the ending bank is empty meaning that this is the root_node.
        """
        _starting_bank = list(_node[0])
        _ending_bank = list(_node[1])

        return (
                       (0 < _starting_bank.count('m') < _starting_bank.count('c')) or
                       (0 < _ending_bank.count('m') < _ending_bank.count('c')) or
                       len(_starting_bank) == 0
               ), len(_starting_bank) == 0, len(_ending_bank) == 0

    def build_graph(_g, _node):
        """
        It starts with the root node and applies all possible operators on each. It then repeats the same process
        recursively for the resulting nodes using them as root nodes. If a new node can not be created because of an
        inapplicable operator or if it already is part of the graph, then it is skipped. An edge is created between
        the parent node and the resulting nodes. This process also sets the flags of each node in its data dict.

        :param _g: A graph object that will be populated with nodes and edges.
        :param _node: The root node to place in the beginning of the graph.
        """
        for op in operators:
            new_node = cross_river(_node[0], _node[1], op)
            if (new_node is not None) and (not _g.has_edge(_node, new_node)):
                _g.add_edge(_node, new_node)

                _is_bad, is_goal, is_root = get_flags(_node)
                _g.nodes[_node]['is_bad'] = False if is_goal else _is_bad
                _g.nodes[_node]['is_goal'] = is_goal
                _g.nodes[_node]['is_root'] = is_root

                _is_bad, is_goal, is_root = get_flags(new_node)
                _g.nodes[new_node]['is_bad'] = False if is_goal else _is_bad
                _g.nodes[new_node]['is_goal'] = is_goal
                _g.nodes[new_node]['is_root'] = is_root

                if not _is_bad:
                    build_graph(_g, new_node)

    def set_levels(_g, _node, _level=0):
        """
        It traverses the nodes of the whole graph recursively, and adds sets their level representing the least number
        of ancestors since the root_node. It traverses the graph in a depth first manner, which means that this function
        also replaces the level value that is already assigned to a node if on a later recursion the same node can be
        shifted to a higher level (smaller value). 0 is the top level indicating the root node. If these levels are used
        when calculating the positions for the plot markers, the graph will be displayed in a tree-like structure
        instead of the usual scattered node (spring) network.

        :param _g: The graph of which the node levels will be set.
        :param _node: The node that's the parent node of each recursion. The root_node should be supplied on the first
                      call.
        :param _level: The current recursion level. This argument should not be passed on first call and it is only
                       to be used by the function itself.
        """
        if 'level' not in _g.nodes[_node].keys() or _level < _g.nodes[_node]['level']:
            _g.nodes[_node]['level'] = _level
        for neighbor in _g.neighbors(_node):
            if 'level' not in _g.nodes[neighbor].keys():
                set_levels(_g, neighbor, _level + 1)
            elif _level + 1 < _g.nodes[neighbor]['level']:
                _g.nodes[neighbor]['level'] = _level + 1
                set_levels(_g, neighbor, _level + 1)

    def get_goal_node(_g):
        """
        Iterates through all nodes of the graph and returns the first node with it's 'is_goal' data set to True.

        :param _g: The graph whose goal node to return
        :return: The node that indicates the goal of the graph, flagged as 'is_goal' when building the graph.
        """
        for _node in list(_g.nodes)[::-1]:
            if _g.nodes[_node]['is_goal']:
                return _node

    def set_heuristic_weights(_g, _node, weight=0):
        """
        Iterate through all nodes of the graph, and set their straight line distance from the provided _node.
        The goal node should be passed on the first call. For each parent node (_node) - neighbor a weight is
        assigned to the edge connecting them which is the current recursion level + 1. Since all nodes can be traversed
        recursively from any node, their recursion level is actually the distance from that node.

        :param _g: The graph whose edges to calculate the heuristic weights for.
        :param _node: The _node that this recursion will set the weights with its neighbors.
        :param weight: The current recursion level. This argument should not be passed on first call and it is only
                       to be used by the function itself.
        """
        if weight == 0:
            for edge in _g.edges:
                _g.edges[edge]['weight'] = 0

        for neighbor in _g.neighbors(_node):
            current_weight = _g[_node][neighbor]['weight']
            if current_weight > weight + 1 or current_weight == 0:
                _g[_node][neighbor]['weight'] = weight + 1
                set_heuristic_weights(_g, neighbor, weight + 1)

    build_graph(g, root_node)
    set_levels(g, root_node)
    goal_node = get_goal_node(g)
    set_heuristic_weights(g, goal_node)
    return g, root_node


def prepare_plot_data(_g):
    """
    Calculates the position of each node of the graph, assigns it a color and a label in order for it to be plotted
    correctly in the desired plot. It uses the node level in order to position the nodes in a tree-like manner.

    :param _g: The graph whose nodes to calculate the plot data.
    :return: A tuple containing all the information required for this graph to be plotted correctly.
    """

    level_counts = {}
    pos = {}
    color_map = []
    labels = {}
    for node in _g.nodes(data=True):
        node_data = node[1]
        _node = node[0]
        starting_bank = list(_node[0])
        ending_bank = list(_node[1])
        level = node_data['level']
        if node_data['is_root']:
            color_map.append('deepskyblue')
        elif node_data['is_goal']:
            color_map.append('limegreen')
        elif node_data['is_bad']:
            color_map.append('orangered')
        else:
            color_map.append('gold')

        label = "{}{}{}{}{}{}".format(starting_bank.count('m'), starting_bank.count('c'),
                                      ('b' if 'b' in starting_bank else ''), ending_bank.count('m'),
                                      ending_bank.count('c'), ('b' if 'b' in ending_bank else ''))
        labels[_node] = label

        if level not in level_counts.keys():
            level_counts[level] = 0

        level_counts[level] += 1

    nodes_in_level = {}
    for node in _g.nodes(data=True):
        node_data = node[1]
        _node = node[0]
        level = node_data['level']

        if level not in nodes_in_level.keys():
            nodes_in_level[level] = 0

        nodes_in_level[level] += 1

        x = (100 / (level_counts[level] + 1) * nodes_in_level[level])
        y = level * 10
        pos[_node] = (x, - y)

    return pos, color_map, labels


def filter_graph_copy(_g, nodes_to_keep):
    """
    Deep-copies the graph into a new object but keeps only the desired nodes. It deletes the nodes not specified in the
    passed list, along with their data and all the edges connected to them.

    :param _g: The graph to copy.
    :param nodes_to_keep: The list of nodes to keep.
    :return: A graph that has all desired nodes and data of the original one.
    """
    new_g = deepcopy(_g)

    nodes_to_remove = []
    for node in new_g.nodes:
        if node not in nodes_to_keep:
            nodes_to_remove.append(node)

    new_g.remove_nodes_from(nodes_to_remove)
    return new_g


def align_positions(pos_origin, pos_target):
    """
    Copies the position of each node from one list to the other.

    :param pos_origin: The positions to keep.
    :param pos_target: The list containing the nodes with the current positions that need to be replaced.
    :return: A list with all the nodes from the pos target list and their positions from the pos origin list.
    """
    aligned_pos = {k: pos_origin[k] for k in pos_target}
    return aligned_pos


def draw_network(_g, pos, color_map, labels, node_size=1250, font_size=8, draw_weights=False):
    """
    Draws the network's nodes, edges and labels in the active plot.

    :param _g: The graph to draw.
    :param pos: The list with node positions for the nodes of the graph.
    :param color_map: The list with node colors for the nodes of the graph.
    :param labels: The list with node labels for the nodes of the graph.
    :param node_size: The size of the node. Default value = 1250 for the default plot dpi.
    :param font_size: The size of the label font. Default value = 8 for the default plot dpi.
    :param draw_weights: A flag indicating whether to draw the edge weight number over each line in the plot.
    """
    nx.draw_networkx_nodes(_g, pos, node_color=color_map, node_size=node_size)
    nx.draw_networkx_edges(_g, pos, alpha=0.2)
    nx.draw_networkx_labels(_g, pos, labels, font_size=font_size)
    if draw_weights:
        nx.draw_networkx_edge_labels(_g, pos, edge_labels=nx.get_edge_attributes(_g, 'weight'))


def clear_axes(axes):
    """
    Removes the x and y ticks from all the passed axes.

    :param axes: The axes whose ticks to remove.
    """
    for ax in axes:
        ax.set_xticks([])
        ax.set_yticks([])


def add_legend(legend_elements, axis, pos):
    """
    Add the supplied legends to the supplied axis on the specified position.

    :param legend_elements: The legends to add.
    :param axis: The axis to add the legends to.
    :param pos: The position of the legend box relative to the axis.
    """
    axis.legend(handles=legend_elements, bbox_to_anchor=pos)


if __name__ == "__main__":
    problem_graph()
