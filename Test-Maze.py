import streamlit as st
import numpy as np
from collections import deque

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

class MazeProblem:
    def __init__(self, board, initial, goal):
        self.board = board
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        x, y = state
        actions = []
        moves = [("up", (x, y - 1)), ("down", (x, y + 1)), ("left", (x - 1, y)), ("right", (x + 1, y))]
        for action, (new_x, new_y) in moves:
            if 0 <= new_y < len(self.board) and 0 <= new_x < len(self.board[0]) and self.board[new_y][new_x] != "#":
                actions.append((action, (new_x, new_y)))
        return actions

    def is_goal(self, state):
        return state == self.goal

def bfs(problem):
    queue = deque([(problem.initial, [])])
    visited = set()

    while queue:
        current_state, path = queue.popleft()

        if current_state in visited:
            continue
        visited.add(current_state)

        if problem.is_goal(current_state):
            return path + [current_state]

        for action, next_state in problem.actions(current_state):
            if next_state not in visited:
                queue.append((next_state, path + [current_state]))

    return None

# Streamlit application
if __name__ == "__main__":
    st.title("Giải mã mê cung")

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
            # Run BFS
            path = bfs(MazeProblem(MAP, start_point, end_point))

            if path:
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
                        elif (x, y) in path:
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
