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

def breadth_first_search_maze_solver():
    # The queue holds lists of: [row_index, column_index, number_of_steps_taken]
    squares_to_visit_queue = [[0, 0, 0]] 
    already_visited_squares = []
    
    # We will count how many squares we actually step on to compare with A*
    nodes_expanded_count = 0
    
    while len(squares_to_visit_queue) > 0:
        current_square = squares_to_visit_queue.pop(0)
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
        
        # Directions are [change_in_row, change_in_column]: Down, Up, Right, Left
        possible_movement_directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        
        for direction in possible_movement_directions:
            new_row = current_row + direction[0]
            new_column = current_column + direction[1]
            
            # Ensure we do not step outside the 10x10 maze boundaries
            if 0 <= new_row <= 9 and 0 <= new_column <= 9:
                # Ensure the square is a path (0), not a wall (1)
                if maze_grid[new_row][new_column] == 0:
                    squares_to_visit_queue.append([new_row, new_column, number_of_steps_taken + 1])

# Run the function and save the two returned variables
bfs_path_length, bfs_nodes_expanded = breadth_first_search_maze_solver()
print(f"BFS Path Length: {bfs_path_length} steps")
print(f"BFS Squares Checked (Nodes Expanded): {bfs_nodes_expanded}")