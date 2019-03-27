from dfs import solve_dfs
from a_star import solve_a_star
from graph import problem_graph

if __name__ == "__main__":
    import os

    if not os.path.exists('dist'):
        os.makedirs('dist')

    prob_graph = problem_graph()
    solve_dfs(*prob_graph)
    solve_a_star(*prob_graph)
