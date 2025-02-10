import pygame
import time
import json
import os
import random

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
BLOCK_SIZE = 40  # Block size for the maze
FPS = 15

# Define Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (169, 169, 169)


# Load the maze data from a JSON file
def load_maps():
    if os.path.exists('mapy/maps.json'):
        with open('mapy/maps.json', 'r') as f:
            data = json.load(f)
        return data['maps']
    return []


# Get a random maze from the list of available maps
def get_random_map():
    maps = load_maps()
    if maps:
        return random.choice(maps)
    return []


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
def draw_maze(maze):
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if maze[y][x] == 1:  # Wall
                pygame.draw.rect(screen, BLACK, pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            elif maze[y][x] == 3:  # Exit
                pygame.draw.rect(screen, GREEN, pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    # Draw the player at its current position (after updating position)
    pygame.draw.rect(screen, RED, pygame.Rect(player_x * BLOCK_SIZE, player_y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))


# Function to handle movement
def move_player(key, maze):
    global player_x, player_y
    if key == pygame.K_UP and maze[player_y - 1][player_x] != 1:
        player_y -= 1
    elif key == pygame.K_DOWN and maze[player_y + 1][player_x] != 1:
        player_y += 1
    elif key == pygame.K_LEFT and maze[player_y][player_x - 1] != 1:
        player_x -= 1
    elif key == pygame.K_RIGHT and maze[player_y][player_x + 1] != 1:
        player_x += 1


# Function to check if the player reached the exit
def check_exit(maze):
    if maze[player_y][player_x] == 3:
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
    if not os.path.exists('times.json'):
        with open('times.json', 'w') as f:
            json.dump({}, f)

    try:
        with open('times.json', 'r') as f:
            existing_times = json.load(f)
    except json.JSONDecodeError:
        existing_times = {}

    if player_name not in existing_times or existing_times[player_name] > time_taken:
        existing_times[player_name] = time_taken

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
            return {}
    else:
        return {}


# Function to display the fastest times (removed from the end of the game)
def display_times():
    times = load_times()
    sorted_times = sorted(times.items(), key=lambda x: x[1])  # Sort by time
    y_offset = 250
    for name, time in sorted_times:
        time_text = font.render(f"{name}: {time:.2f} seconds", True, BLACK)
        screen.blit(time_text, (100, y_offset))
        y_offset += 40


# Function to run the game
def run_game(maze):
    global player_x, player_y
    # Reset player position to start
    player_x = 1
    player_y = 1
    running = True
    start_time = time.time()

    while running:
        screen.fill(WHITE)
        draw_maze(maze)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                move_player(event.key, maze)

        if check_exit(maze):
            end_time = time.time() - start_time
            return end_time

        pygame.display.update()
        clock.tick(FPS)


# Function to display play again options
def play_again():
    font_large = pygame.font.Font(None, 60)
    font_small = pygame.font.Font(None, 40)

    running = True
    while running:
        screen.fill(WHITE)

        # Draw "Play Again" message
        message = font_large.render("Play Again?", True, BLACK)
        screen.blit(message, (SCREEN_WIDTH // 2 - message.get_width() // 2, SCREEN_HEIGHT // 4))

        # Draw options
        same_map_text = font_small.render("Press 1 to play the same map", True, BLACK)
        random_map_text = font_small.render("Press 2 for a random map", True, BLACK)
        screen.blit(same_map_text, (SCREEN_WIDTH // 2 - same_map_text.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(random_map_text, (SCREEN_WIDTH // 2 - random_map_text.get_width() // 2, SCREEN_HEIGHT // 2 + 40))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()  # Close the game entirely when clicking X

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 'same'  # Return the same map option
                elif event.key == pygame.K_2:
                    return 'random'  # Return random map option

    return 'random'  # Default to random if no key is pressed


# Main loop
if __name__ == '__main__':
    player_name = get_player_name()  # Get the name from the player
    print(f"Welcome, {player_name}!")

    # Choose a random map to start
    current_map = get_random_map()

    while True:
        print("Solve the maze to record your time.")
        fastest_time = run_game(current_map)

        save_time(player_name, fastest_time)

        # Ask if the player wants to play again
        choice = play_again()

        if choice == 'same':
            # Keep the same map
            pass
        elif choice == 'random':
            # Get a new random map
            current_map = get_random_map()

    pygame.quit()
