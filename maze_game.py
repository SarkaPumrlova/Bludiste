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
SCREEN = (236, 200, 252)
PLAYER = (254, 123, 212)
END = (194, 3, 253)
GRAY = (169, 169, 169)
WALL = (34, 22, 44)

# Load the maze data from a JSON file
def load_maps():
    if os.path.exists(''
                      'maps.json'):
        with open('maps.json', 'r') as f:
            data = json.load(f)
        return data['maps']
    return []

# Get a random maze from the list of available maps
def get_random_map():
    maps = load_maps()
    if maps:
        return random.choice(maps)
    return []

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
                pygame.draw.rect(screen, WALL, pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            elif maze[y][x] == 3:  # Exit
                pygame.draw.rect(screen, END, pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    # Draw the player at its current position (after updating position)
    pygame.draw.rect(screen, PLAYER, pygame.Rect(player_x * BLOCK_SIZE, player_y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

# Function to handle movement
def move_player(key, maze):
    global player_x, player_y
    if key == pygame.K_UP and player_y > 0 and maze[player_y - 1][player_x] != 1:
        player_y -= 1
    elif key == pygame.K_DOWN and player_y < len(maze) - 1 and maze[player_y + 1][player_x] != 1:
        player_y += 1
    elif key == pygame.K_LEFT and player_x > 0 and maze[player_y][player_x - 1] != 1:
        player_x -= 1
    elif key == pygame.K_RIGHT and player_x < len(maze[0]) - 1 and maze[player_y][player_x + 1] != 1:
        player_x += 1

# Function to check if the player reached the exit
def check_exit(maze):
    return maze[player_y][player_x] == 3

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

# Function to run the game
def run_game(maze):
    global player_x, player_y
    # Reset player position to start
    player_x = 1
    player_y = 1
    running = True
    start_time = time.time()

    while running:
        screen.fill(SCREEN)
        draw_maze(maze)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                move_player(event.key, maze)

        if check_exit(maze):
            return time.time() - start_time

        pygame.display.update()
        clock.tick(FPS)

# Function to display play again options
def play_again():
    font_large = pygame.font.Font(None, 60)
    font_small = pygame.font.Font(None, 40)

    while True:
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

        # Process events to check for key presses or quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()  # Exit the game if the window is closed

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 'same'  # Return 'same' when 1 is pressed
                elif event.key == pygame.K_2:
                    return 'random'  # Return 'random' when 2 is pressed

        # Pause for 30 milliseconds to prevent high CPU usage
        clock.tick(30)

# Main loop
if __name__ == '__main__':
    player_name = get_player_name()  # Get the name from the player
    print(f"Welcome, {player_name}!")

    # Choose a random map to start
    current_map = get_random_map()

    while True:
        print("Solve the maze to record your time.")
        fastest_time = run_game(current_map)

        # Ask if the player wants to play again
        choice = play_again()

        if choice == 'same':
            # Keep the same map
            print("Playing again with the same map.")
            continue  # This will loop back and keep the same map
        elif choice == 'random':
            # Get a new random map
            print("Playing again with a new random map.")
            current_map = get_random_map()
            continue  # This will loop back and get a new map

pygame.quit()
