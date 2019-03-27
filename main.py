from dfs import solve_dfs
from a_star import solve_a_star

if __name__ == "__main__":
    import os

    if not os.path.exists('dist'):
        os.makedirs('dist')

    solve_dfs()
    solve_a_star()