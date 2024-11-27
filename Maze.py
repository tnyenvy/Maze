import streamlit as st
import math
from simpleai.search import SearchProblem, astar

# Define cost of moving around the map
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

        new_state = (x, y)
        return new_state

    def is_goal(self, state):
        return state == self.goal

    def cost(self, state, action, state2):
        return COSTS[action]

    def heuristic(self, state):
        x, y = state
        gx, gy = self.goal
        return math.sqrt((x - gx) ** 2 + (y - gy) ** 2)

# Streamlit UI
st.set_page_config(page_title="Maze Solver", layout="wide")
st.title("Maze Solver App")
st.markdown("### Welcome to the Maze Solver! Use the tool below to visualize and solve a maze.")

# Display the maze map
st.markdown("#### Original Maze Map")
st.text_area("Maze Map", MAP, height=200)

# Convert map to a list
MAP = [list(x) for x in MAP.split("\n") if x]

# Create maze solver object
problem = MazeSolver(MAP)

# Run the solver
result = astar(problem, graph_search=True)

# Extract the path
path = [x[1] for x in result.path()]

# Display the solved maze
st.markdown("#### Solved Maze")
solved_maze = ""
for y in range(len(MAP)):
    for x in range(len(MAP[y])):
        if (x, y) == problem.initial:
            solved_maze += '🟢'  # Use an emoji to represent the start point
        elif (x, y) == problem.goal:
            solved_maze += '❌'  # Use an emoji to represent the goal
        elif (x, y) in path:
            solved_maze += '·'  # Use a different symbol for the path
        else:
            solved_maze += MAP[y][x]
    solved_maze += "\n"

# Display the solution in a styled text area
st.text_area("Solution", solved_maze, height=300)

# Add a footer for additional information
st.markdown("---")
st.markdown("**Developed by**: Your Name")
st.markdown("**References**: A. Artasanchez, P. Joshi, *Artificial Intelligence with Python, 2nd Edition, Packt, 2020*")
