import heapq
import itertools
import time

GOAL_STATE = (1, 2, 3,
              4, 5, 6,
              7, 8, 0)


def get_neighbors(state):
    """Return list of (new_state, move) reachable by sliding a tile
    into the blank (0) position."""
    neighbors = []
    idx = state.index(0)
    row, col = divmod(idx, 3)

    moves = {
        'UP':    (row - 1, col),
        'DOWN':  (row + 1, col),
        'LEFT':  (row, col - 1),
        'RIGHT': (row, col + 1),
    }

    for move, (r, c) in moves.items():
        if 0 <= r < 3 and 0 <= c < 3:
            new_idx = r * 3 + c
            new_state = list(state)
            new_state[idx], new_state[new_idx] = new_state[new_idx], new_state[idx]
            neighbors.append((tuple(new_state), move))

    return neighbors


def manhattan_distance(state, goal=GOAL_STATE):
    """Sum of Manhattan distances of each tile from its goal position."""
    distance = 0
    for value in range(1, 9):
        cur_idx = state.index(value)
        goal_idx = goal.index(value)
        cur_row, cur_col = divmod(cur_idx, 3)
        goal_row, goal_col = divmod(goal_idx, 3)
        distance += abs(cur_row - goal_row) + abs(cur_col - goal_col)
    return distance


def is_solvable(state):
    """8-puzzle is solvable only if the number of inversions is even."""
    tiles = [t for t in state if t != 0]
    inversions = 0
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            if tiles[i] > tiles[j]:
                inversions += 1
    return inversions % 2 == 0


def reconstruct_path(came_from, current):
    path = [current]
    moves = []
    while current in came_from:
        current, move = came_from[current]
        path.append(current)
        moves.append(move)
    path.reverse()
    moves.reverse()
    return path, moves


def print_board(state):
    for i in range(0, 9, 3):
        row = state[i:i + 3]
        print(" ".join(str(x) if x != 0 else "_" for x in row))
    print()


def a_star_search(start, goal=GOAL_STATE, heuristic=manhattan_distance):
    counter = itertools.count()  # tie-breaker for heap comparisons
    open_list = [(heuristic(start, goal), 0, next(counter), start)]
    came_from = {}
    g_score = {start: 0}
    visited = set()
    nodes_expanded = 0

    while open_list:
        f, g, _, current = heapq.heappop(open_list)

        if current in visited:
            continue
        visited.add(current)
        nodes_expanded += 1

        if current == goal:
            path, moves = reconstruct_path(came_from, current)
            return path, moves, nodes_expanded

        for neighbor, move in get_neighbors(current):
            tentative_g = g_score[current] + 1
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                came_from[neighbor] = (current, move)
                f_score = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_list, (f_score, tentative_g, next(counter), neighbor))

    return None, None, nodes_expanded  # no solution found


if __name__ == "__main__":
    start_state = (3, 2, 6,
                   0, 1, 8,
                   5, 4, 7)

    print("Start state:")
    print_board(start_state)
    print("Goal state:")
    print_board(GOAL_STATE)

    if not is_solvable(start_state):
        print("This puzzle configuration is NOT solvable.")
    else:
        start_time = time.time()
        path, moves, nodes_expanded = a_star_search(start_state)
        end_time = time.time()

        print(f"Solution found in {len(moves)} moves")
        print(f"Nodes expanded : {nodes_expanded}")
        print(f"Time taken     : {end_time - start_time:.5f} seconds")
        print(f"Move sequence  : {moves}\n")

        print("Step-by-step path:")
        for i, state in enumerate(path):
            print(f"Step {i}:")
            print_board(state)
