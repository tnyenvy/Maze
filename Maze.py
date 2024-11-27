import streamlit as st
import math
import matplotlib.pyplot as plt
import numpy as np
from simpleai.search import SearchProblem, astar

# Define the cost of moving around the map
cost_regular = 1.0
cost_diagonal = 1.7

# Create the cost dictionary
COSTS = {
    "up": cost_regular,
    "down": cost_regular,
    "left": cost_regular,
    "right": cost_regular,
}

# Define the map
MAP = """
##############################
#         #              #   #
# ####    ########       #   #
#  o #    #              #   #
#    ###     #####  ######   #
#      #   ###   #           #
#      #     #   #  #  #   ###
#     #####    #    #  # x   #
#              #       #     #
##############################
"""

# Class containing the methods to solve the maze
class MazeSolver(SearchProblem):
    def __init__(self, board):
        self.board = board
        self.goal = (0, 0)

        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x].lower() == "o":
                    self.initial = (x, y)
                elif self.board[y][x].lower() == "x":
                    self.goal = (x, y)

        super(MazeSolver, self).__init__(initial_state=self.initial)

    def actions(self, state):
        actions = []
        for action in COSTS.keys():
            newx, newy = self.result(state, action)
            if self.board[newy][newx] != "#":
                actions.append(action)
        return actions

    def result(self, state, action):
        x, y = state
        if action == "up":
            y -= 1
        elif action == "down":
            y += 1
        elif action == "left":
            x -= 1
        elif action == "right":
            x += 1
        return (x, y)

    def is_goal(self, state):
        return state == self.goal

    def cost(self, state, action, state2):
        return COSTS[action]

    def heuristic(self, state):
        x, y = state
        gx, gy = self.goal
        return math.sqrt((x - gx) ** 2 + (y - gy) ** 2)

if __name__ == "__main__":
    st.title("Maze Solver")

    # Convert map to a list
    MAP = [list(x) for x in MAP.split("\n") if x]

    # Create maze solver object
    problem = MazeSolver(MAP)

    # Run the solver
    result = astar(problem, graph_search=True)

    # Extract the path
    path = [x[1] for x in result.path()]

    # Create a 2D array to display the maze
    maze_display = np.array(MAP)
    maze_path = maze_display.copy()

    # Mark the path in the maze
    for y in range(len(MAP)):
        for x in range(len(MAP[y])):
            if (x, y) in path:
                maze_path[y][x] = '·'

    # Display the maze using Matplotlib
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(maze_path == '#', cmap='gray', interpolation='none')
    for y in range(len(maze_path)):
        for x in range(len(maze_path[y])):
            if maze_path[y][x] == '·':
                ax.text(x, y, '·', color='red', ha='center', va='center')
            elif maze_path[y][x] == 'o':
                ax.text(x, y, 'o', color='green', ha='center', va='center')
            elif maze_path[y][x] == 'x':
                ax.text(x, y, 'x', color='blue', ha='center', va='center')

    ax.set_xticks(np.arange(0, len(maze_path[0]), 1))
    ax.set_yticks(np.arange(0, len(maze_path), 1))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.grid(color='black', linestyle='-', linewidth=1)
    st.pyplot(fig)