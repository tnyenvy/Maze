import streamlit as st
from aima3.search import Problem, breadth_first_search
import numpy as np

# Define the map with obstacles and walls
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

# Convert map to a 2D list
MAP = [list(row) for row in MAP.split("\n") if row]


# Define the MazeProblem class compatible with AIMA
class MazeProblem(Problem):
    def __init__(self, initial, goal, board):
        super().__init__(initial, goal)
        self.board = board

    def actions(self, state):
        """Return possible moves from the current state."""
        x, y = state
        moves = [
            ("up", (x, y - 1)),
            ("down", (x, y + 1)),
            ("left", (x - 1, y)),
            ("right", (x + 1, y)),
        ]
        valid_actions = []
        for action, (nx, ny) in moves:
            if 0 <= ny < len(self.board) and 0 <= nx < len(self.board[0]) and self.board[ny][nx] != "#":
                valid_actions.append((action, (nx, ny)))
        return valid_actions

    def result(self, state, action):
        """Return the resulting state after applying an action."""
        return action[1]

    def goal_test(self, state):
        """Check if the current state is the goal."""
        return state == self.goal


# Streamlit application
if __name__ == "__main__":
    st.title("Giải mã mê cung (BFS - AIMA)")

    # Display the maze as an image using ASCII art
    st.subheader("Mẫu mê cung:")
    for row in MAP:
        st.text("".join(row))

    st.subheader("Vui lòng chọn điểm Xuất phát (S) và Đích đến (E):")

    # Allow user to select start and end points
    start_x = st.number_input("Chọn tọa độ X cho điểm Xuất phát", min_value=0, max_value=len(MAP[0]) - 1, step=1)
    start_y = st.number_input("Chọn tọa độ Y cho điểm Xuất phát", min_value=0, max_value=len(MAP) - 1, step=1)
    end_x = st.number_input("Chọn tọa độ X cho Đích đến", min_value=0, max_value=len(MAP[0]) - 1, step=1)
    end_y = st.number_input("Chọn tọa độ Y cho Đích đến", min_value=0, max_value=len(MAP) - 1, step=1)

    start_point = (int(start_x), int(start_y))
    end_point = (int(end_x), int(end_y))

    # Validate the user inputs
    if st.button("Tìm đường"):
        if MAP[start_point[1]][start_point[0]] == "#" or MAP[end_point[1]][end_point[0]] == "#":
            st.error("Điểm Xuất phát hoặc Đích đến nằm trên vật cản. Vui lòng chọn lại!")
        elif start_point == end_point:
            st.error("Điểm Xuất phát và Đích đến phải khác nhau!")
        else:
            # Solve the maze using BFS from AIMA
            problem = MazeProblem(start_point, end_point, MAP)
            solution = breadth_first_search(problem)

            if solution:
                path = [node for node in solution.path()]
                st.success("Đã tìm được đường đi hợp lý!")

                # Create an HTML representation of the maze with colors
                maze_html = """
                <style>
                .maze {
                    display: grid;
                    grid-template-columns: repeat(30, 20px);
                    gap: 2px;
                    border: 5px solid red;
                    padding: 10px;
                    background-color: #fff;
                }
                .cell {
                    width: 20px;
                    height: 20px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    border: 1px solid #ddd;
                }
                .wall {
                    background-color: black;
                    color: white;
                }
                .start {
                    background-color: green;
                    color: white;
                }
                .end {
                    background-color: red;
                    color: white;
                }
                .path {
                    background-color: magenta;
                    color: white;
                }
                .empty {
                    background-color: white;
                }
                </style>
                <div class="maze">
                """

                for y in range(len(MAP)):
                    for x in range(len(MAP[y])):
                        if (x, y) == start_point:
                            maze_html += '<div class="cell start">S</div>'
                        elif (x, y) == end_point:
                            maze_html += '<div class="cell end">E</div>'
                        elif (x, y) in [state for action, state in path]:
                            maze_html += '<div class="cell path">·</div>'
                        elif MAP[y][x] == '#':
                            maze_html += '<div class="cell wall">#</div>'
                        else:
                            maze_html += '<div class="cell empty">.</div>'

                maze_html += "</div>"

                # Display the maze with the path highlighted
                st.markdown(maze_html, unsafe_allow_html=True)
            else:
                st.error("Rất tiếc, không thể tìm được đường đi. Vui lòng thử lại!")
