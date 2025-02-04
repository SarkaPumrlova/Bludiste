import pygame
import time
import json
import os

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
BLOCK_SIZE = 40  # Block size for the maze
FPS = 15

# Define Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (169, 169, 169)

# Maze definition (0 = open space, 1 = wall, 2 = player start, 3 = exit)
MAZE = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 1, 0, 0, 1],
    [1, 1, 1, 1, 0, 1, 1, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 3, 1, 1]  # Exit is at position (7, 8)
]

# Initialize player position
player_x = 1
player_y = 1

# Set up screen and clock
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Maze Game')
clock = pygame.time.Clock()

# Define font for text input and display
font = pygame.font.Font(None, 40)

# Function to draw the maze and player
def draw_maze():
    for y in range(len(MAZE)):
        for x in range(len(MAZE[y])):
            if MAZE[y][x] == 1:  # Wall
                pygame.draw.rect(screen, BLACK, pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            elif MAZE[y][x] == 3:  # Exit
                pygame.draw.rect(screen, GREEN, pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    # Draw the player at its current position (after updating position)
    pygame.draw.rect(screen, RED, pygame.Rect(player_x * BLOCK_SIZE, player_y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

# Function to handle movement
def move_player(key):
    global player_x, player_y
    if key == pygame.K_UP and MAZE[player_y - 1][player_x] != 1:
        player_y -= 1
    elif key == pygame.K_DOWN and MAZE[player_y + 1][player_x] != 1:
        player_y += 1
    elif key == pygame.K_LEFT and MAZE[player_y][player_x - 1] != 1:
        player_x -= 1
    elif key == pygame.K_RIGHT and MAZE[player_y][player_x + 1] != 1:
        player_x += 1

# Function to check if the player reached the exit
def check_exit():
    if MAZE[player_y][player_x] == 3:
        return True
    return False

# Function to handle name input
def get_player_name():
    name = ""
    input_active = True
    while input_active:
        screen.fill(WHITE)

        # Draw the input box
        pygame.draw.rect(screen, GRAY, pygame.Rect(100, 150, 400, 50))
        name_text = font.render(name, True, BLACK)
        screen.blit(name_text, (110, 160))

        # Instructions text
        prompt_text = font.render("Enter your name and press Enter", True, BLACK)
        screen.blit(prompt_text, (120, 100))

        pygame.display.update()

        # Capture events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name != "":  # Finish name entry
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]  # Remove last character
                else:
                    name += event.unicode  # Add typed character

    return name

# Function to save the fastest time
def save_time(player_name, time_taken):
    # Ensure times.json file exists
    if not os.path.exists('times.json'):
        with open('times.json', 'w') as f:
            json.dump({}, f)  # Create an empty JSON file if it doesn't exist

    # Load existing times
    try:
        with open('times.json', 'r') as f:
            existing_times = json.load(f)
    except json.JSONDecodeError:
        existing_times = {}  # If the file is corrupted, use an empty dict

    # Update the times
    if player_name not in existing_times or existing_times[player_name] > time_taken:
        existing_times[player_name] = time_taken

    # Write updated times back to the file
    with open('times.json', 'w') as f:
        json.dump(existing_times, f)

# Function to load the fastest times
def load_times():
    if os.path.exists('times.json'):
        try:
            with open('times.json', 'r') as f:
                times = json.load(f)
            return times
        except json.JSONDecodeError:
            return {}  # Return an empty dictionary if there's an error reading the file
    else:
        return {}  # Return an empty dictionary if the file doesn't exist

# Function to display fastest times on the screen
def display_times():
    times = load_times()
    sorted_times = sorted(times.items(), key=lambda x: x[1])  # Sort by time
    y_offset = 250  # Start y position for displaying times
    for name, time in sorted_times:
        time_text = font.render(f"{name}: {time:.2f} seconds", True, BLACK)
        screen.blit(time_text, (100, y_offset))
        y_offset += 40

# Main function to run the game
def run_game():
    global player_x, player_y
    running = True
    start_time = time.time()

    while running:
        screen.fill(WHITE)
        draw_maze()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                move_player(event.key)

        if check_exit():
            end_time = time.time() - start_time
            return end_time

        display_times()  # Display leaderboard
        pygame.display.update()
        clock.tick(FPS)

# Main loop
if __name__ == '__main__':
    player_name = get_player_name()  # Get the name from the player
    print(f"Welcome, {player_name}!")

    print("Solve the maze to record your time.")
    fastest_time = run_game()

    pygame.quit()
