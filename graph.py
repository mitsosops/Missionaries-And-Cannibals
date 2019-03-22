import networkx as nx
from copy import deepcopy

def problem_graph():
    starting_bank = sorted(['m', 'm', 'm', 'c', 'c', 'c', 'b'])
    ending_bank = []


    operators = sorted([sorted(l) for l in [['m'],
                                            ['c'],
                                            ['m', 'm'],
                                            ['c', 'c'],
                                            ['m', 'c']]])


    def build_node(_starting_bank, _ending_bank):
        _node = (tuple(sorted(_starting_bank)), tuple(sorted(_ending_bank)))
        return _node


    G = nx.Graph()

    root_node = build_node(starting_bank, ending_bank)


    def cross_river(_starting_bank, _ending_bank, operator):
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


    def is_final(_node):
        _starting_bank = list(_node[0])
        _ending_bank = list(_node[1])

        return (
                    (0 < _starting_bank.count('m') < _starting_bank.count('c')) or
                    (0 < _ending_bank.count('m') < _ending_bank.count('c')) or
                    len(_starting_bank) == 0
            ), len(_starting_bank) == 0,  len(_ending_bank) == 0


    def build_graph(_g, _node):
        for op in operators:
            new_node = cross_river(_node[0], _node[1], op)
            if (new_node is not None) and (not _g.has_edge(_node, new_node)):
                _g.add_edge(_node, new_node)
                                
                _is_final, is_result, is_root = is_final(_node)
                _g.nodes[_node]['is_final'] = _is_final
                _g.nodes[_node]['is_result'] = is_result
                _g.nodes[_node]['is_root'] = is_root

                _is_final, is_result, is_root = is_final(new_node)
                _g.nodes[new_node]['is_final'] = _is_final
                _g.nodes[new_node]['is_result'] = is_result
                _g.nodes[new_node]['is_root'] = is_root

                if not _is_final:
                    build_graph(_g, new_node)


    def set_levels(_g, _node, _level=0):
        if 'level' not in _g.nodes[_node].keys() or _level < _g.nodes[_node]['level']:
            _g.nodes[_node]['level'] = _level
        for neighbor in _g.neighbors(_node):
            if 'level' not in _g.nodes[neighbor].keys():
                set_levels(_g, neighbor, _level + 1)
            elif _level + 1 < _g.nodes[neighbor]['level']:
                _g.nodes[neighbor]['level'] = _level + 1
                set_levels(_g, neighbor, _level + 1)


    build_graph(G, root_node)
    set_levels(G, root_node)
    return G, root_node


def prepare_plot_data(_g):
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
        elif node_data['is_result']:
            color_map.append('limegreen')
        elif node_data['is_final']:
            color_map.append('orangered')
        else:
            color_map.append('gold')

        label = (str(starting_bank.count('m')) + str(starting_bank.count('c')) + ('b' if 'b' in starting_bank else '') +
                str(ending_bank.count('m')) + str(ending_bank.count('c')) + ('b' if 'b' in ending_bank else ''))
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
    new_g = deepcopy(_g)

    nodes_to_remove = []
    for node in new_g.nodes:
        if node not in nodes_to_keep:
            nodes_to_remove.append(node)
    
    new_g.remove_nodes_from(nodes_to_remove)
    return new_g
        

def align_positions(pos_origin, pos_target):
    aligned_pos = {k: pos_origin[k] for k in pos_target }
    return aligned_pos
