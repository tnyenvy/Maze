import streamlit as st
import math
from simpleai.search import SearchProblem, astar

# Define cost of moving around the map
cost_regular = 1.0

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

class MazeSolver(SearchProblem):
    def __init__(self, board):
        self.board = board
        self.goal = (0, 0)
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x] == 'o':
                    self.initial = (x, y)
                elif self.board[y][x] == 'x':
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
        if action == "up": y -= 1
        elif action == "down": y += 1
        elif action == "left": x -= 1
        elif action == "right": x += 1
        return (x, y)

    def is_goal(self, state):
        return state == self.goal

    def cost(self, state, action, state2):
        return COSTS[action]

    def heuristic(self, state):
        x, y = state
        gx, gy = self.goal
        return math.sqrt((x - gx) ** 2 + (y - gy) ** 2)

# Main function to display the maze and solution on Streamlit
if __name__ == "__main__":
    st.title("Maze Solver")

    # Convert map to a list of lists
    MAP = [list(row) for row in MAP.split("\n") if row]

    # Create maze solver object
    problem = MazeSolver(MAP)

    # Run the solver using A* algorithm
    result = astar(problem, graph_search=True)
    path = [x[1] for x in result.path()]

    # Display the maze with the path
    st.write("Maze Solution:")
    for y in range(len(MAP)):
        row = ""
        for x in range(len(MAP[y])):
            if (x, y) == problem.initial:
                row += 'o'
            elif (x, y) == problem.goal:
                row += 'x'
            elif (x, y) in path:
                row += '·'
            else:
                row += MAP[y][x]
        st.text(row)
