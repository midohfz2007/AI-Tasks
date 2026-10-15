import time

# The winning state we want to reach. 0 represents the empty sliding space.
goal_board_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)

# ==========================================
# 1. THE THREE HEURISTICS (GUESSING METHODS)
# ==========================================

def heuristic_1_misplaced_tiles(current_board_state):
    # Counts how many tiles are simply in the wrong spot.
    wrong_tiles_count = 0
    for index in range(9):
        if current_board_state[index] != 0 and current_board_state[index] != goal_board_state[index]:
            wrong_tiles_count = wrong_tiles_count + 1
    return wrong_tiles_count

def heuristic_2_manhattan_distance(current_board_state):
    # Calculates the physical distance each tile is away from its correct spot.
    total_distance = 0
    for index in range(9):
        tile_number = current_board_state[index]
        if tile_number != 0:
            # Find current row and column (using simple math: divide by 3 for row, remainder for column)
            current_row = index // 3
            current_column = index % 3
            
            # Find where this tile SHOULD be in the goal board
            goal_index = goal_board_state.index(tile_number)
            goal_row = goal_index // 3
            goal_column = goal_index % 3
            
            # Add the distance between where it is and where it should be
            distance = abs(current_row - goal_row) + abs(current_column - goal_column)
            total_distance = total_distance + distance
    return total_distance

def heuristic_3_manhattan_plus_reversal_penalty(current_board_state):
    # A more complex heuristic. It uses Manhattan distance, but adds a heavy penalty 
    # if two tiles are right next to each other but in the reverse order.
    score = heuristic_2_manhattan_distance(current_board_state)
    
    # Check rows for reversed tiles next to each other (e.g., 2 followed by 1)
    for row in range(3):
        for col in range(2): # Only check first and second column to avoid going out of bounds
            current_index = (row * 3) + col
            right_neighbor_index = current_index + 1
            
            tile_a = current_board_state[current_index]
            tile_b = current_board_state[right_neighbor_index]
            
            # If both aren't empty, and they belong in this row but are swapped, penalize them!
            if tile_a != 0 and tile_b != 0:
                if (tile_a - 1) // 3 == row and (tile_b - 1) // 3 == row: # Both belong in this row
                    if tile_a > tile_b: # They are in the wrong order
                        score = score + 2 # Add penalty
    return score

# ==========================================
# 2. HELPER TO CATCH UNSOLVABLE BOARDS
# ==========================================
def is_board_solvable(board_state):
    # Half of all random 8-puzzle boards are mathematically impossible to solve.
    # We count "inversions" (how many times a larger number appears before a smaller one).
    # If the number of inversions is odd, the puzzle is impossible.
    inversions_count = 0
    for i in range(9):
        for j in range(i + 1, 9):
            if board_state[i] != 0 and board_state[j] != 0 and board_state[i] > board_state[j]:
                inversions_count = inversions_count + 1
    return inversions_count % 2 == 0

# ==========================================
# 3. THE A* ALGORITHM
# ==========================================

def a_star_8_puzzle_solver(starting_board_state, chosen_heuristic_function):
    if not is_board_solvable(starting_board_state):
        return "Unsolvable", 0
        
    start_time = time.time()
    
    starting_heuristic_guess = chosen_heuristic_function(starting_board_state)
    
    # Queue holds: [board_state, number_of_steps_taken, total_estimated_score]
    boards_to_visit_priority_queue = [[starting_board_state, 0, starting_heuristic_guess]] 
    already_visited_boards = set() # Using a set here so the computer checks it instantly
    nodes_expanded_count = 0
    
    while len(boards_to_visit_priority_queue) > 0:
        # Sort the line so the lowest total_estimated_score (index 2) is at the front
        boards_to_visit_priority_queue.sort(key=lambda data: data[2])
        
        current_data = boards_to_visit_priority_queue.pop(0)
        current_board = current_data[0]
        number_of_steps_taken = current_data[1]
        
        if current_board == goal_board_state:
            time_taken = time.time() - start_time
            return time_taken, nodes_expanded_count
            
        if current_board in already_visited_boards:
            continue
            
        already_visited_boards.add(current_board)
        nodes_expanded_count = nodes_expanded_count + 1
        
        # Find where the empty space (0) is
        empty_space_index = current_board.index(0)
        empty_row = empty_space_index // 3
        empty_column = empty_space_index % 3
        
        possible_movement_directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        
        for direction in possible_movement_directions:
            new_row = empty_row + direction[0]
            new_column = empty_column + direction[1]
            
            if 0 <= new_row <= 2 and 0 <= new_column <= 2:
                new_empty_index = (new_row * 3) + new_column
                
                # Create a new board by swapping the empty space with the target tile
                board_as_list = list(current_board)
                # Swap them
                board_as_list[empty_space_index], board_as_list[new_empty_index] = board_as_list[new_empty_index], board_as_list[empty_space_index]
                new_board_state = tuple(board_as_list) # Convert back to tuple so it can go in the set
                
                if new_board_state not in already_visited_boards:
                    new_steps_taken = number_of_steps_taken + 1
                    future_steps_guess = chosen_heuristic_function(new_board_state)
                    total_estimated_score = new_steps_taken + future_steps_guess
                    
                    boards_to_visit_priority_queue.append([new_board_state, new_steps_taken, total_estimated_score])
                    
    return "Failed", nodes_expanded_count

# ==========================================
# 4. RUNNING THE TESTS ON 5 STATES
# ==========================================

# 1. Very Easy (2 moves away)
state_1 = (1, 8, 5, 4, 6, 2, 7, 3, 0)
# 2. Medium (6 moves away)
state_2 = (0, 1, 8, 4, 6, 5, 7, 3, 2)
# 3. Harder (10 moves away)
state_3 = (4, 1, 8, 7, 6, 5, 0, 3, 2)
# 4. Unsolvable (Swapped 7 and 8)
state_4 = (1, 2, 3, 4, 5, 6, 8, 7, 0)
# 5. Unsolvable (Randomly mixed)
state_5 = (8, 1, 2, 0, 4, 3, 7, 6, 5)

test_states = [state_1, state_2, state_3, state_4, state_5]
heuristics = [
    ("H1 (Misplaced)", heuristic_1_misplaced_tiles),
    ("H2 (Manhattan)", heuristic_2_manhattan_distance),
    ("H3 (Complex)", heuristic_3_manhattan_plus_reversal_penalty)
]

for i, state in enumerate(test_states):
    print(f"\n--- Testing Initial State {i+1} ---")
    print(f"Board Layout: {state[:3]} \n              {state[3:6]} \n              {state[6:]}")
    
    for heuristic_name, heuristic_func in heuristics:
        time_taken, nodes = a_star_8_puzzle_solver(state, heuristic_func)
        if time_taken == "Unsolvable":
            print(f"[{heuristic_name}] Result: UNSOLVABLE BOARD CONFIGURATION")
            break # Skip checking other heuristics if it's impossible
        else:
            print(f"[{heuristic_name}] Nodes Checked: {nodes} | Time Taken: {time_taken:.4f} seconds")