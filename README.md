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
### A* solution steps graphs
![A* solution steps graphs][img4]

The label of each node is the textual representation of its state. Each state can be represented by 4 digits and the letter "b".
1. The first digit represents the number of missionaries on the starting river bank.
2. The second digit represents the number of cannibals on the startring river bank.
3. The third digit represents the number of missionaries on the destination's river bank.
4. The fourth digit represents the number of cannibals on the destination's river bank. 
5. The letter "b" follows the second digit if the boat is at the starting river bank or the fourth digit if the boat is at the destination's river bank.

The following image shows the state depicted by the node labeled as 32b01
![mcexample][img5]

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
[img4]: https://github.com/mitsosops/Missionaries-And-Cannibals/raw/master/documentation/A_Star_Solution_Steps_Figure.png "A* solution steps graphs"
[img5]: https://github.com/mitsosops/Missionaries-And-Cannibals/raw/master/documentation/mcexample.png "Missionaries and Cannibals label example"
[4]: https://github.com/bndr/pipreqs