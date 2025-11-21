import pygame
from constants import WIDTH, HEIGHT, BLACK, GREEN, BLUE, RED
from game_utils import draw_grid, draw_block, spawn_food
from snake_class import Snake

def main():
    pygame.init()
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Smart Snake AI Duel")
    clock = pygame.time.Clock()

    snakeA = Snake(BLUE, (5,5), is_smart=True)
    snakeB = Snake(RED, (15,15), is_smart=False)

    snakes = [snakeA, snakeB]
    food = spawn_food(snakes)

    running = True
    frame = 0
    MAX_FRAMES = 2000

    while running:
        clock.tick(40)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        frame += 1

        # move snakes
        snakeA.move(snakes, food)
        snakeB.move(snakes, food)

        # if food eaten
        if snakeA.head() == food or snakeB.head() == food:
            food = spawn_food(snakes)

        # end if both die or too long
        if (not snakeA.alive and not snakeB.alive) or frame >= MAX_FRAMES:
            running = False

        # DRAW
        WIN.fill(BLACK)
        draw_grid(WIN)

        draw_block(WIN, GREEN, food)

        for s in snakes:
            for p in s.body:
                draw_block(WIN, s.color, p)

        pygame.display.update()

    # Keep window open until user closes it
    print("Game Over. Close the window to exit.")
    waiting = True
    while waiting:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False

    pygame.quit()

    # RESULTS
    print("\n===== FINAL SCORES =====")
    print("Blue Smart Snake (A):", snakeA.score)
    print("Red Q-Learning Snake (B):", snakeB.score)
    print("========================\n")

if __name__ == "__main__":
    main()
