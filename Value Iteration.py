
# Set the discount factor
gamma = 0.9

# Store all possible positions in the grid (except the obstacle)
states = [(1,1), (1,2), (1,3),
          (2,1), (2,3),
          (3,1), (3,2), (3,3)]

# Define the goal and obstacle positions
goal = (3,3)
obstacle = (2,2)

# Store the four possible actions
actions = {
    "up": (-1, 0),       # Move up one row
    "down": (1, 0),      # Move down one row
    "left": (0, -1),     # Move left one column
    "right": (0, 1)      # Move right one column
}

# Give every position an initial value of zero
V = {}

for state in states:
    V[state] = 0

# Repeat the value calculations 100 times
for i in range(100):

    # Create a copy of the old values
    new_V = V.copy()

    # Check every position
    for state in states:

        # Skip the goal because it is the final position
        if state == goal:
            continue

        # Store the highest value found
        best_value = -1000

        # Try all four possible actions
        for action in actions:

            # Get the row and column movement
            dr, dc = actions[action]

            # Calculate the next position
            nr = state[0] + dr
            nc = state[1] + dc

            # Check if the robot moves outside the grid
            if nr < 1 or nr > 3 or nc < 1 or nc > 3:
                next_state = state
                reward = -5

            # Check if the robot moves into the obstacle
            elif (nr, nc) == obstacle:
                next_state = state
                reward = -5

            else:
                # Update the robot's position
                next_state = (nr, nc)

                # Give a reward if the robot reaches the goal
                if next_state == goal:
                    reward = 10
                else:
                    # Give a small penalty for normal movement
                    reward = -1

            # Calculate the value of this action
            value = reward + gamma * V[next_state]

            # Keep the highest value
            if value > best_value:
                best_value = value

        # Save the best value for this position
        new_V[state] = best_value

    # Update all the values for the next iteration
    V = new_V

# Display the final values
print("Final State Values:")

for state in states:
    print(state, "=", round(V[state], 2))

# Display the best action for each position
print("\nOptimal Actions:")

for state in states:

    # No action is needed at the goal
    if state == goal:
        continue

    best_value = -1000
    best_action = ""

    # Check all four possible actions again
    for action in actions:

        dr, dc = actions[action]

        nr = state[0] + dr
        nc = state[1] + dc

        # Check for invalid movements
        if nr < 1 or nr > 3 or nc < 1 or nc > 3 or (nr, nc) == obstacle:
            next_state = state
            reward = -5
        else:
            next_state = (nr, nc)

            if next_state == goal:
                reward = 10
            else:
                reward = -1

        # Calculate the action's value
        value = reward + gamma * V[next_state]

        # Save the action if it has a higher value
        if value > best_value:
            best_value = value
            best_action = action

    # Print the best action
    print(state, "->", best_action)
