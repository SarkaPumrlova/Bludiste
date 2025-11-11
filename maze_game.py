import pygame
import time
import json
import os
import random

import sqlite3

# save times and names
def save_top_time(player_name, final_time):
    conn = sqlite3.connect("game_data.db")
    cursor = conn.cursor()

    # Insert into the correct columns
    cursor.execute("INSERT INTO top_times (player_name, time) VALUES (?, ?)", (player_name, final_time))

    conn.commit()
    conn.close()



# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
FPS = 15
BLOCK_SIZE = 40

# Define Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SCREEN = (236, 200, 252)
PLAYER = (254, 123, 212)
END = (194, 3, 253)
GRAY = (169, 169, 169)
WALL = (34, 22, 44)
STAR_COLOR = (255,255,0)

stars_collected = 0


# Load the maze data from a JSON file
def load_maps():
    if os.path.exists('maps.json'):
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

def count_stars(maze): #spočítá hvězdičky v mapě
    return sum(row.count(2) for row in maze)

# Set up screen and clock
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Maze Game')
clock = pygame.time.Clock()

# Define font for text input and display
font = pygame.font.Font(None, 40)

# Player starting position
player_x = 1
player_y = 1

# Function to draw the maze and player
def draw_maze(maze):
    global BLOCK_SIZE
    maze_width = len(maze[0])  # Počet sloupců
    maze_height = len(maze)  # Počet řádků

    # Dynamické nastavení velikosti bloku podle obrazovky
    BLOCK_SIZE = min(SCREEN_WIDTH // maze_width, SCREEN_HEIGHT // maze_height)

    for y in range(maze_height):
        global total_stars
        for x in range(maze_width):
            rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            if maze[y][x] == 1:
                pygame.draw.rect(screen, WALL, rect)
            elif maze[y][x] == 3:
                pygame.draw.rect(screen, END, rect)
            elif maze[y][x] == 2:  # Hvězdička
                pygame.draw.circle(screen, STAR_COLOR, rect.center, BLOCK_SIZE // 3)

    pygame.draw.rect(screen, PLAYER, pygame.Rect(player_x * BLOCK_SIZE, player_y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

# Function to handle movement
def move_player(key, maze):
    global player_x, player_y, stars_collected
    new_x, new_y = player_x, player_y

    if key == pygame.K_UP and player_y > 0 and maze[player_y - 1][player_x] != 1:
        new_y -= 1
    elif key == pygame.K_DOWN and player_y < len(maze) - 1 and maze[player_y + 1][player_x] != 1:
        new_y += 1
    elif key == pygame.K_LEFT and player_x > 0 and maze[player_y][player_x - 1] != 1:
        new_x -= 1
    elif key == pygame.K_RIGHT and player_x < len(maze[0]) - 1 and maze[player_y][player_x + 1] != 1:
        new_x += 1

    # Pokud hráč narazí na hvězdičku, sbírá ji
    if maze[new_y][new_x] == 2:
        stars_collected += 1
        maze[new_y][new_x] = 0  # Odstraníme hvězdičku z mapy

    player_x, player_y = new_x, new_y

# Function to check if the player reached the exit
#def check_exit(maze):
    #return maze[player_y][player_x] == 3





def check_exit(maze):
    global player_x, player_y # Zajištění přístupu ke globálním proměnným

    # Ověření, že souřadnice hráče jsou v platném rozsahu bludiště
    #if 0 <= player_y < len(maze) and 0 <= player_x < len(maze[0]):
        #return maze[player_y][player_x] == 3  # Kontrola, zda je hráč na východu

    #return False  # Pokud jsou souřadnice mimo rozsah, vrátí False
    if stars_collected < total_stars:
        return False  # Hráč ještě nesebral všechny hvězdičky
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


# Function to run the game with a live timer floating on the right
def run_game(maze):
    global player_x, player_y
    player_x, player_y = 1, 1
    running = True
    start_time = time.time()

    while running:
        screen.fill(SCREEN)
        draw_maze(maze)

        elapsed_time = time.time() - start_time
        formatted_time = f"Time: {elapsed_time:.2f} sec"

        font_timer = pygame.font.Font(None, 50)
        timer_text = font_timer.render(formatted_time, True, WHITE)
        text_width, _ = timer_text.get_size()
        screen.blit(timer_text, (SCREEN_WIDTH - text_width - 20, 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                move_player(event.key, maze)

        if check_exit(maze):
            return elapsed_time  # Return final time when the player reaches the exit

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
    global total_stars
    player_name = get_player_name()  # Get the name from the player
    print(f"Welcome, {player_name}!")

    current_map = get_random_map()
    total_stars = count_stars(current_map)

    while True:
        print("Solve the maze to record your time.")
        final_time = run_game(current_map)

        if final_time is None:
            break


        # Function to show final time before asking to play again
        def show_final_time(final_time):
            font_large = pygame.font.Font(None, 80)
            while True:
                screen.fill(WHITE)

                # Display the final time
                final_text = font_large.render(f"Finished in {final_time:.2f} sec!", True, BLACK)
                screen.blit(final_text, (SCREEN_WIDTH // 2 - final_text.get_width() // 2, SCREEN_HEIGHT // 3))

                pygame.display.update()
                pygame.time.delay(2000)  # Show for 2 seconds
                return  # Exit after delay


        # Save the player's result in the database
        save_top_time(player_name, final_time)

        # Show final time and ask to play again
        show_final_time(final_time)
        choice = play_again()

        if choice == 'same':
            continue
        elif choice == 'random':
            current_map = get_random_map()
            continue







pygame.quit()