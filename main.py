import pygame
from game import GameState
from story import Story
from ui import UI

def main():
    print("Initializing Pygame...")
    pygame.init()
    pygame.mixer.init()
    # Initialize components
    print("Creating game state, story, and UI...")
    state = GameState()
    story = Story()
    ui = UI()
    clock = pygame.time.Clock()
    # Load initial scene
    print(f"Loading initial scene: {state.current_scene}")
    story.load_scene(state, state.current_scene)
    # Main loop
    print("Starting main loop...")
    while True:
        current_time = pygame.time.get_ticks()
        # Handle input
        choice_rects, mouse_pos = ui.handle_input(state, story)
        # Update typewriter
        ui.update_typewriter(state, current_time)
        # Render
        ui.render(state, choice_rects, mouse_pos)
        clock.tick(60)

if __name__ == "__main__":
    main()
