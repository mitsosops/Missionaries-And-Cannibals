# Missionaries-And-Cannibals

## Implementation
This project implements and uses the blind DFS and the heuristic A* solvers for the Missionaries and Cannibals problem.

## Report
* [report.pdf][1]
* [report.docx][2]

## Prerequisites
* [Python 3.x][3] installed

## Preparation
[Optional] Add python to path.

After downloading or cloning the repository start a terminal in the project root and run the following command:
`pip install -r requirements.txt`

## Execution
The solvers generate their results as images inside the `dist` directory in project root. The `dist` directory is automatically created if it doesn't exist.

To run both solvers execute the command `python main.py` in a terminal in project root.

To run only one of the solvers, execute the command `python dfs.py` or the command `python a_star.py` in a terminal in project root.

## Results
### DFS problem and solution graphs
![DFS problem and solution graphs][img1]
### DFS solution steps graphs
![DFS solution steps graphs][img2]
### A* problem and solution graphs
![A* problem and solution graphs][img3]
### A* problem and solution graphs
![A* problem and solution graphs][img4]

## Dependencies
* matplotlib (tested with v3.0.3)
* networkx (tested with v2.2)

## Miscellaneous
The requirments.txt was auto-generated using [pipreqs][4]


[1]: https://github.com/mitsosops/Missionaries-And-Cannibals/raw/master/documentation/report.pdf
[2]: https://github.com/mitsosops/Missionaries-And-Cannibals/raw/master/documentation/report.docx
[3]: https://www.python.org/
[img1]: https://github.com/mitsosops/Missionaries-And-Cannibals/raw/master/documentation/DFS_Problem_Solution_Figure.png "DFS problem and solution graphs"
[img2]: https://github.com/mitsosops/Missionaries-And-Cannibals/raw/master/documentation/DFS_Solution_Steps_Figure.png "DFS solution steps graphs"
[img3]: https://github.com/mitsosops/Missionaries-And-Cannibals/raw/master/documentation/A_Star_Problem_Solution_Figure.png "A* problem and solution graphs"
[img4]: https://github.com/mitsosops/Missionaries-And-Cannibals/raw/master/documentation/A_Star_Solution_Steps_Figure.png "A* problem and solution graphs"
[4]: https://github.com/bndr/pipreqs