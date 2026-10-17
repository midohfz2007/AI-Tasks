# 0 is a clear path, 1 is a solid wall. Start is top-left (0,0), End is bottom-right (9,9)
maze_grid = [ 
    [0, 0, 1, 0, 0, 0, 1, 0, 0, 0], # Row 0: 0s are paths, 1s are walls. Start is at index 0,0
    [1, 0, 1, 0, 1, 0, 0, 1, 0, 1], # Row 1 of the maze grid
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0], # Row 2 of the maze grid
    [0, 1, 0, 1, 0, 0, 1, 0, 1, 0], # Row 3 of the maze grid
    [0, 1, 0, 0, 0, 1, 0, 0, 1, 0], # Row 4 of the maze grid
    [0, 0, 1, 1, 0, 1, 0, 1, 0, 0], # Row 5 of the maze grid
    [1, 0, 0, 1, 0, 0, 0, 1, 0, 1], # Row 6 of the maze grid
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 0], # Row 7 of the maze grid
    [0, 1, 1, 1, 0, 0, 1, 1, 1, 0], # Row 8 of the maze grid
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0]  # Row 9 of the maze grid. End is at index 9,9
]

def breadth_first_search_maze_solver(): 
    # The queue holds lists of: [row_index, column_index, number_of_steps_taken]
    squares_to_visit_queue = [[0, 0, 0]] # Initialize the queue with the starting position (0,0) and 0 steps
    already_visited_squares = [] # Initialize an empty list to keep track of squares we have already explored
    
    # Dictionary to remember the path taken (stores the parent of each square)
    parent = {} # Initialize an empty dictionary to store which square led to the current square

    # We will count how many squares we actually step on to compare with A*
    nodes_expanded_count = 0 # Initialize a counter to track how many squares we process
    
    while len(squares_to_visit_queue) > 0: # Continue looping as long as there are squares left to visit in the queue
        current_square = squares_to_visit_queue.pop(0) # Remove and get the first item from the queue (FIFO - First In, First Out)
        current_row = current_square[0] # Extract the row index from the current item
        current_column = current_square[1] # Extract the column index from the current item
        number_of_steps_taken = current_square[2] # Extract the current number of steps taken from the start
        
        current_position = (current_row, current_column) # Create a tuple of the current coordinates for easier reference
        
        # Check if we have reached the bottom-right corner
        if current_row == 9 and current_column == 9: # Check if the current row and column match the destination (9, 9)
            
            # Rebuild the path backwards using the parent dictionary
            path = [] # Initialize an empty list to store the final path coordinates
            position = current_position # Start backtracking from the destination position
            
            while position != (0, 0): # Continue looping backwards until we reach the starting position (0, 0)
                path.append(position) # Add the current position to the path list
                position = parent[position] # Update the position to its parent (the square we came from)
            
            path.append((0, 0)) # Add the starting position (0, 0) to the path since the loop stops right before it
            path.reverse()      # Reverse the list so the path goes from start to end, rather than end to start
            
            return number_of_steps_taken, nodes_expanded_count, path # Exit the function and return the final steps, expanded count, and the path list
            
        # Prevent stepping on the same square twice
        if [current_row, current_column] in already_visited_squares: # Check if we have already processed this specific square
            continue # If visited, skip the rest of this loop iteration and move to the next item in the queue
            
        # Mark this square as visited and increase our counter
        already_visited_squares.append([current_row, current_column]) # Add the current square to our list of visited squares
        nodes_expanded_count = nodes_expanded_count + 1 # Increment the expanded nodes counter by 1
        
        # Directions are [change_in_row, change_in_column]: Down, Up, Right, Left
        possible_movement_directions = [[1, 0], [-1, 0], [0, 1], [0, -1]] # Define the 4 possible movement directions (down, up, right, left)
        
        for direction in possible_movement_directions: # Loop through each of the 4 possible directions
            new_row = current_row + direction[0] # Calculate the new row index by adding the row change
            new_column = current_column + direction[1] # Calculate the new column index by adding the column change
            new_position = (new_row, new_column) # Create a tuple for the new theoretical position
            
            # Ensure we do not step outside the 10x10 maze boundaries
            if 0 <= new_row <= 9 and 0 <= new_column <= 9: # Check if the new coordinates are within the grid bounds (0 to 9)
                # Ensure the square is a path (0), not a wall (1)
                if maze_grid[new_row][new_column] == 0: # Check if the grid value at the new position is 0 (an open path)
                    
                    # Record where we came from if we haven't seen this square before
                    if new_position not in parent and new_position != (0, 0): # Check if the new position is unvisited and not the start
                        parent[new_position] = current_position # Map the new position to the current position (its parent) in the dictionary
                        
                    squares_to_visit_queue.append([new_row, new_column, number_of_steps_taken + 1]) # Add the new valid square to the end of the queue, incrementing the step count
                    
    return -1, nodes_expanded_count, [] # If the queue empties and no path is found, return -1 steps, the expanded count, and an empty path

# New function to visualize the maze and the path
def draw_maze(path): # Define a function that takes the solved path list as an argument
    for row in range(10): # Loop through each row index from 0 to 9
        line = "" # Initialize an empty string to build the printed row characters
        
        for column in range(10): # Loop through each column index from 0 to 9
            position = (row, column) # Create a tuple of the current coordinate being drawn
            
            if position == (0, 0): # Check if the current coordinate is the starting position
                line += "S "        # Append an 'S' to represent the Start
            elif position == (9, 9): # Check if the current coordinate is the ending position
                line += "E "        # Append an 'E' to represent the End
            elif position in path: # Check if the current coordinate is part of the solved path
                line += "* "        # Append an '*' to represent the path taken
            elif maze_grid[row][column] == 1: # Check if the original grid coordinate is a wall
                line += "# "        # Append a '#' to represent a solid wall
            else: # If it's none of the above (just an empty, unused path)
                line += ". "        # Append a '.' to represent an unused open path
                
        print(line) # Print the fully constructed string line for the current row

# Run the function and save the returned variables (now includes path)
bfs_path_length, bfs_nodes_expanded, bfs_path = breadth_first_search_maze_solver() # Call the solver function and unpack the 3 returned values into variables

if bfs_path_length != -1: # Check if a valid path was found (length is not -1)
    print(f"BFS Path Length: {bfs_path_length} steps") # Print the total number of steps taken to reach the end
    print(f"BFS Nodes Expanded: {bfs_nodes_expanded}") # Print the total number of squares checked during the search
    
    print("\nPath coordinates:") # Print a header for the coordinate list
    print(bfs_path) # Print the list of coordinate tuples making up the path
    
    print("\nMaze with BFS path:") # Print a header for the visual maze drawing
    draw_maze(bfs_path) # Call the draw function, passing the found path to it
else: # If the path length is -1 (meaning no path was found)
    print("No path found!") # Print an error message stating no path exists
