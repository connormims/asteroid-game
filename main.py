import pygame
import sys
from astroidfield import AsteroidField
from asteroid import Asteroid
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_state, log_event
from player import Player
from shot import Shot
from leaderboard import save_score, load_leaderboard, display_leaderboard

def main():
    print("Starting Asteroids with pygame version: 3.13")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    game_over = False
    viewing_leaderboard = False

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.font.init()

    score = 0
    player_name = ""
    input_active = True

    font = pygame.font.SysFont("Arial", 24)
    large_font = pygame.font.SysFont("Arial", 72)
    score_font = pygame.font.SysFont("Arial", 36)

    clock = pygame.time.Clock()
    dt = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    AsteroidField.containers = (updatable,)
    Asteroid.containers = (updatable, drawable, asteroids)
    Player.containers = (updatable, drawable)
    Shot.containers = (updatable, drawable, shots)

    player = Player(SCREEN_WIDTH / 2,SCREEN_HEIGHT / 2)
    af = AsteroidField()

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
            # --- HANDLING NAME INPUT ---
            if game_over and input_active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Submit the name and save the score
                        save_score(player_name if player_name else "AAA", score)
                        input_active = False # Stop typing once submitted
                    elif event.key == pygame.K_BACKSPACE:
                        # Remove the last character
                        player_name = player_name[:-1]
                    else:
                        # Add the character (limit length to 3-10 characters)
                        if len(player_name) < 10:
                            player_name += event.unicode

            # --- HANDLING MENU NAVIGATION (After name is saved) ---
            elif game_over and (input_active == False):
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b and viewing_leaderboard:
                        viewing_leaderboard = False
                    elif not viewing_leaderboard:
                        if event.key == pygame.K_r:
                            # Restart game
                            score = 0
                            player_name = "" 
                            game_over = False
                            viewing_leaderboard = False
                            input_active = True     
                            for a in asteroids:
                                a.kill()
                            for s in shots:
                                s.kill()
                            player.reset() 
                        if event.key == pygame.K_l:
                            # Show leaderboard
                            viewing_leaderboard = True
                        if event.key == pygame.K_ESCAPE:
                            # Exit game
                            sys.exit()

        # --- 1. LOGIC ---
        if not game_over:
            updatable.update(dt)
            for a in asteroids:
                if a.collides_with(player):
                    log_event("player_hit")
                    game_over = True
                for s in shots:
                    if s.collides_with(a):
                        log_event("asteroid_shot")
                        s.kill()
                        a.split()
                        score += 10

        # --- 2. DRAWING ---
        screen.fill("black")

        # Draw all sprites first
        for sprite in drawable:
            sprite.draw(screen)

        # Draw the score in the corner
        score_surface = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_surface, (10, 10))

        # Draw the Game Over overlay ON TOP of everything else
        if game_over:
            # Draw a semi-transparent or solid box
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(180) # Semi-transparent
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0,0))

            # --- INPUT SCREEN ---
            if input_active:
                prompt_surf = score_font.render("Enter Username:", True, (255, 255, 255))
                screen.blit(prompt_surf, (SCREEN_WIDTH/2 - 120, SCREEN_HEIGHT/2 - 100))
        
                # Draw the name buffer (with a cursor)
                name_surf = score_font.render(f"{player_name}_", True, (0, 255, 0))
                screen.blit(name_surf, (SCREEN_WIDTH/2 - 120, SCREEN_HEIGHT/2 - 60 ))

            # --- LEADERBOARD SCREEN ---
            elif viewing_leaderboard:
                display_leaderboard(screen, SCREEN_WIDTH, SCREEN_HEIGHT, score_font, font)
                
                back_surf = font.render("Press 'B' to Go Back", True, (200, 200, 200))
                back_rect = back_surf.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT - 50))
                screen.blit(back_surf, back_rect)
            
            # --- MENU SCREEN ---
            else:
                over_surface = large_font.render("GAME OVER", True, (255, 0, 0))
                screen.blit(over_surface, (SCREEN_WIDTH/2 - 220, SCREEN_HEIGHT/2 - 100))

                final_score_surface = score_font.render(f"Final Score: {score}", True, (255, 255, 255))
                screen.blit(final_score_surface, (SCREEN_WIDTH/2 - 130, SCREEN_HEIGHT/2 - 20))

                retry_surface = score_font.render("Press 'R' to Restart", True, (200, 200, 200))
                screen.blit(retry_surface, (SCREEN_WIDTH/2 - 175, SCREEN_HEIGHT/2 + 20))

                lb_surface = score_font.render("Press 'L' for Leaderboard", True, (200, 200, 200))
                screen.blit(lb_surface, (SCREEN_WIDTH/2 - 215, SCREEN_HEIGHT/2 + 60))

                quit_surface = score_font.render("Press 'Esc' to Quit", True, (200, 200, 200))
                screen.blit(quit_surface, (SCREEN_WIDTH/2 - 170, SCREEN_HEIGHT/2 + 100))

        pygame.display.flip()
        fps = clock.tick(60)
        dt = fps / 1000

if __name__ == "__main__":
    main()
