# 0 is a clear path, 1 is a solid wall. Start is top-left (0,0), End is bottom-right (9,9)
maze_grid = [
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
    [1, 1, 0, 1, 1, 1, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    [1, 1, 0, 1, 1, 1, 1, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
]


def calculate_manhattan_distance_heuristic(current_row, current_column):
    # Calculates the physical blocks remaining to reach row 9, column 9
    return abs(9 - current_row) + abs(9 - current_column)

def a_star_maze_solver():
    starting_heuristic_guess = calculate_manhattan_distance_heuristic(0, 0)
    
    # The queue holds lists of: [row_index, column_index, number_of_steps_taken, total_estimated_score]
    squares_to_visit_priority_queue = [[0, 0, 0, starting_heuristic_guess]] 
    already_visited_squares = []
    
    # We will count how many squares we actually step on to compare with BFS
    nodes_expanded_count = 0
    
    while len(squares_to_visit_priority_queue) > 0:
        # Sort the queue so the square with the lowest total_estimated_score (index 3) is always at the front
        squares_to_visit_priority_queue.sort(key=lambda square_data: square_data[3])
        
        current_square = squares_to_visit_priority_queue.pop(0)
        current_row = current_square[0]
        current_column = current_square[1]
        number_of_steps_taken = current_square[2]
        
        # Check if we have reached the bottom-right corner
        if current_row == 9 and current_column == 9:
            return number_of_steps_taken, nodes_expanded_count
            
        # Prevent stepping on the same square twice
        if [current_row, current_column] in already_visited_squares:
            continue
            
        # Mark this square as visited and increase our counter
        already_visited_squares.append([current_row, current_column])
        nodes_expanded_count = nodes_expanded_count + 1
        
        possible_movement_directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        
        for direction in possible_movement_directions:
            new_row = current_row + direction[0]
            new_column = current_column + direction[1]
            
            if 0 <= new_row <= 9 and 0 <= new_column <= 9:
                if maze_grid[new_row][new_column] == 0:
                    
                    new_steps_taken = number_of_steps_taken + 1
                    future_steps_guess = calculate_manhattan_distance_heuristic(new_row, new_column)
                    
                    # The A* Formula: f = g + h
                    total_estimated_score = new_steps_taken + future_steps_guess
                    
                    squares_to_visit_priority_queue.append([new_row, new_column, new_steps_taken, total_estimated_score])

# Run the function and save the two returned variables
astar_path_length, astar_nodes_expanded = a_star_maze_solver()
print(f"A* Path Length: {astar_path_length} steps")
print(f"A* Squares Checked (Nodes Expanded): {astar_nodes_expanded}")