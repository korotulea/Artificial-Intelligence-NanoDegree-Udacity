# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A:  The conventional search techniques to solve any puzzle may quickly run into combinatorial exponential growth and explosion. 
Sudoku is a puzzle in that at any time will always be one or more squares whose value is constrained to a single value. Thus, each box in the sudoku has a set of legal values that could be in this box. Those legal values could be defined base on so called constrains propagated value from other box from the same unit (row, column, and 3x3 square). The Naked Twins (doubles) means that there are only two options in the two boxes in the same unit (for example 23 in row (square) unit for box A1 and A2). Thus if this collision happened, the box A1 could take value of 2 or 3 only and the box A2 - 3 or 2, respectively. Thus, if Naked Twins are existed in the unit we can eliminate 2 and 3 from all other boxes belong to the same unit, thus simplify the further search tree for the Sudoku solution.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: The meaning of diagonal sudoku is that not only row, column, and 3x3 units have to be constrained to having only '123456789' digits without duplicate, but the main diagonals A1-I9 and A9-I1 have to follow the same rule. In order to solve this type of Sudoku, we just need to add two more units into the unitlist, thus all the programmed constrains and search would be taking into account the main diagonals too. My solution were programmed to use three constrains techniques for diagonal Sudoku (5 types of units), which are: 
* Eliminate Strategy:  if a square has only one possible value, then eliminate that value from the square's peers. 
* Only choice: if a unit has only one possible place for a value, then put the value there.
* Naked Twins: if there are naked twins in the unit, then eliminate naked twins values from the over boxes in this unit.  

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.